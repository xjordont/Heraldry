#target "indesign"
/* Explicitly run this packaged script. No startup hooks, event listeners or PDFs. */
(function () {
    var settings = /*HERALDRY_SETTINGS*/;
    var folder = File($.fileName).parent;
    var nativeFile = File(folder.fsName + "/" + settings.native);
    var roundtripFile = File(folder.fsName + "/" + settings.roundtrip);
    var reportFile = File(folder.fsName + "/native-report.json");
    var oldInteraction = app.scriptPreferences.userInteractionLevel;
    var oldRedraw = app.scriptPreferences.enableRedraw;
    var doc = null;
    var report = {status: "FAILED", source_sha256: settings.source_sha256, export_id: settings.export_id,
        indesign_version: app.version, pages: 0, added_pages: 0,
        missing_fonts: [], missing_links: [], overset_stories: [], overset_cells: [],
        visual_review: "NOT TESTED", physical_print: "NOT TESTED"};

    function quoted(value) {
        return '"' + String(value).replace(/["\\\u0000-\u001f]/g, function (c) {
            if (c === '"') { return '\\"'; }
            if (c === "\\") { return "\\\\"; }
            var code = c.charCodeAt(0).toString(16);
            return "\\u" + ("0000" + code).slice(-4);
        }) + '"';
    }
    function stringify(value) {
        if (value === null) { return "null"; }
        if (typeof value === "string") { return quoted(value); }
        if (typeof value === "number" || typeof value === "boolean") { return String(value); }
        var parts = [], key;
        if (value instanceof Array) {
            for (key = 0; key < value.length; key++) { parts.push(stringify(value[key])); }
            return "[" + parts.join(",") + "]";
        }
        for (key in value) {
            if (value.hasOwnProperty(key)) { parts.push(quoted(key) + ":" + stringify(value[key])); }
        }
        return "{" + parts.join(",") + "}";
    }
    function writeReport() {
        reportFile.encoding = "UTF-8";
        if (!reportFile.open("w")) { throw Error("Cannot write native-report.json"); }
        reportFile.write(stringify(report) + "\n");
        reportFile.close();
    }
    function frameBounds(page) {
        var p = settings.profile.page, b = page.bounds;
        var recto = page.side == PageSideOptions.RIGHT_HAND;
        return [b[0] + p.top, b[1] + (recto ? p.inside : p.outside),
            b[2] - p.bottom, b[3] - (recto ? p.outside : p.inside)];
    }
    function visibleEnd(frame) {
        if (!frame.lines.length) { return -1; }
        var line = frame.lines.lastItem();
        return line.insertionPoints.lastItem().index;
    }
    function inspect(document) {
        var i, j, k, story, table, cell;
        report.missing_fonts = [];
        report.missing_links = [];
        report.overset_stories = [];
        report.overset_cells = [];
        for (i = 0; i < document.fonts.length; i++) {
            if (document.fonts[i].status != FontStatus.INSTALLED) {
                report.missing_fonts.push(document.fonts[i].fullName);
            }
        }
        for (i = 0; i < document.links.length; i++) {
            if (document.links[i].status != LinkStatus.NORMAL) {
                report.missing_links.push(document.links[i].name);
            }
        }
        if (document.links.length !== settings.expected_links) { throw Error("A linked illustration or vector was lost during native import."); }
        for (i = 0; i < document.stories.length; i++) {
            story = document.stories[i];
            if (story.overflows) { report.overset_stories.push(String(story.id)); }
            for (j = 0; j < story.tables.length; j++) {
                table = story.tables[j];
                for (k = 0; k < table.cells.length; k++) {
                    cell = table.cells[k];
                    if (cell.overflows) { report.overset_cells.push(String(table.id) + ":" + cell.name); }
                }
            }
        }
        report.pages = document.pages.length;
        if (report.missing_fonts.length || report.missing_links.length ||
                report.overset_stories.length || report.overset_cells.length) {
            throw Error("Native font/link/overset checks failed; inspect native-report.json. No text was deleted or reduced to fit.");
        }
    }
    // A second invocation must not replace either manual edits or their report.
    if (nativeFile.exists || roundtripFile.exists) { throw Error("Native output exists. Choose a fresh export folder to preserve manual edits."); }
    try {
        if (parseFloat(app.version) < 16) { throw Error("InDesign 16.0 or later is required for this IDML profile."); }
        app.scriptPreferences.userInteractionLevel = UserInteractionLevels.NEVER_INTERACT;
        app.scriptPreferences.enableRedraw = false;
        doc = app.open(File(folder.fsName + "/" + settings.idml), false);
        doc.viewPreferences.horizontalMeasurementUnits = MeasurementUnits.POINTS;
        doc.viewPreferences.verticalMeasurementUnits = MeasurementUnits.POINTS;
        doc.viewPreferences.rulerOrigin = RulerOrigin.PAGE_ORIGIN;
        doc.textPreferences.smartTextReflow = false;
        doc.layers.itemByName("01 Paper").move(LocationOptions.AT_END);
        doc.layers.itemByName("04 Navigation and ornament").move(LocationOptions.AT_BEGINNING);
        var i, j, link, file, page, frame, last, story, before, after, stalled, containers;
        for (i = 0; i < doc.links.length; i++) {
            link = doc.links[i];
            if (!settings.links.hasOwnProperty(link.name)) { throw Error("Unexpected linked resource: " + link.name); }
            file = File(folder.fsName + "/" + settings.links[link.name]);
            if (!file.exists) { throw Error("Missing packaged link: " + file.fsName); }
            link.relink(file);
            link.update();
        }
        // Fit linked source graphics to their native frames without distorting them.
        var items = doc.allPageItems;
        for (i = 0; i < items.length; i++) {
            if (items[i].extractLabel("heraldry-asset") && items[i].allGraphics.length) {
                items[i].fit(items[i].extractLabel("heraldry-asset") === "COVER-FRONT" ?
                    FitOptions.FILL_PROPORTIONALLY : FitOptions.PROPORTIONALLY);
                items[i].fit(FitOptions.CENTER_CONTENT);
            }
        }
        // Replace seed folios with the application's own live page-number marker.
        for (i = 0; i < doc.masterSpreads.length; i++) {
            var masterFrames = doc.masterSpreads[i].textFrames;
            for (j = 0; j < masterFrames.length; j++) {
                if (masterFrames[j].extractLabel("heraldry-furniture") === "folio") {
                    masterFrames[j].contents = SpecialCharacters.AUTO_PAGE_NUMBER;
                }
            }
        }
        doc.recompose();
        // A separate story per chapter keeps navigation and later manual edits local.
        var mainStories = [], seen = {}, frames = doc.textFrames.everyItem().getElements();
        for (i = 0; i < frames.length; i++) {
            var storyKey = frames[i].extractLabel("heraldry-story");
            if (storyKey.indexOf("manuscript_") === 0 && !seen[storyKey]) {
                mainStories.push({key: storyKey, story: frames[i].parentStory});
                seen[storyKey] = true;
            }
        }
        if (mainStories.length !== settings.expected_story_count) { throw Error("A tagged manuscript story was lost during import."); }
        for (i = 0; i < mainStories.length; i++) {
            story = mainStories[i].story;
            stalled = 0;
            while (story.overflows) {
                containers = story.textContainers;
                last = containers[containers.length - 1];
                before = visibleEnd(last);
                if (!last.parentPage || doc.pages.length >= settings.profile.maximum_pages) {
                    throw Error("Cannot complete text flow within the configured page limit: " + mainStories[i].key);
                }
                page = doc.pages.add(LocationOptions.AFTER, last.parentPage);
                page.appliedMaster = doc.masterSpreads.itemByName("A-Heraldry");
                frame = page.textFrames.add(doc.layers.itemByName("03 Editable manuscript"));
                frame.geometricBounds = frameBounds(page);
                frame.textFramePreferences.textColumnCount = settings.profile.page.columns;
                frame.textFramePreferences.textColumnGutter = settings.profile.page.gutter;
                frame.textFramePreferences.insetSpacing = 0;
                frame.insertLabel("heraldry-story", mainStories[i].key);
                frame.previousTextFrame = last;
                doc.recompose();
                report.added_pages++;
                after = visibleEnd(frame);
                stalled = after <= before ? stalled + 1 : 0;
                if (stalled >= 2) { throw Error("A table row or anchored object cannot fit: " + mainStories[i].key + ". Adjust this independent layout; no content was discarded."); }
            }
            // Remove unused trailing seed frames/pages, never a frame holding content.
            containers = story.textContainers;
            while (containers.length > 1 && !containers[containers.length - 1].lines.length) {
                last = containers[containers.length - 1];
                page = last.parentPage;
                if (!page || page.textFrames.length !== 1) { break; }
                page.remove();
                containers = story.textContainers;
            }
        }
        doc.recompose();
        inspect(doc);
        doc.textPreferences.addPages = AddPageOptions.END_OF_STORY;
        doc.textPreferences.limitToMasterTextFrames = false;
        doc.textPreferences.deleteEmptyPages = true;
        doc.textPreferences.smartTextReflow = true;
        doc.save(nativeFile);
        doc.exportFile(ExportFormat.INDESIGN_MARKUP, roundtripFile, false);
        doc.close(SaveOptions.NO);
        doc = null;
        // Reopen the saved native file and run the same checks after serialisation.
        doc = app.open(nativeFile, false);
        doc.recompose();
        inspect(doc);
        doc.close(SaveOptions.NO);
        doc = null;
        report.status = "PASS";
        report.native = settings.native;
        report.roundtrip = settings.roundtrip;
        report.native_bytes = nativeFile.length;
        report.roundtrip_bytes = roundtripFile.length;
        writeReport();
    } catch (error) {
        report.error = String(error);
        writeReport();
        throw error;
    } finally {
        if (doc && doc.isValid) { doc.close(SaveOptions.NO); }
        app.scriptPreferences.userInteractionLevel = oldInteraction;
        app.scriptPreferences.enableRedraw = oldRedraw;
    }
}());
