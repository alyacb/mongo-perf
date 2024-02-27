if (typeof(tests) !== "object") {
    tests = [];
}

(function() {
    "use strict";

    Random.setRandomSeed(258);

    /**
     * Setup: Create a collection of documents containing only an ObjectId _id field.
     *
     * Test: Empty query that returns all documents.
     */
    const nDocs = 100 * 1000;
    // addQueryTestCase({
    //     name: "IxScanFull",
    //     indexes: [{a: 1}],
    //     tags: ["regression"],
    //     nDocs: nDocs,
    //     docs: function(i) {
    //         return {a: i};
    //     },
    //     op: {op: "find", query: {a: {$lte: nDocs}}},
    //     createViewsPassthrough: false,
    //     createAggregationTest: false
    // });

    function addTestCase(name, params) {
        addQueryTestCase({
            name,
            indexes: [{a: 1}],
            tags: ["regression"],
            nDocs: nDocs,
            docs: function(i) {
                return {a: i};
            },
            // docs: smallDoc,
            params, 
            op: {op: "find", query: {a: {$lte: nDocs}}},
            createViewsPassthrough: false,
            createAggregationTest: false
        });
    }

    function testCaseExperiment() {
        addTestCase("IXSCAN_FULL_experiment", {internalSwitchGenerateBatchImpl: 1});
    }

    function testCaseAppendOnly() {
        addTestCase("IXSCAN_FULL_append_only", {internalSwitchGenerateBatchImpl: 3});
    }

    function testCaseBaseline() {
        addTestCase("IXSCAN_FULL_baseline", {internalSwitchGenerateBatchImpl: 0});
    }

    const numTests = 48;
    for (let i=0; i<numTests; i++) {
        // addQueryTestCase({
        //     name: "IxScanFull",
        //     indexes: [{a: 1}],
        //     tags: ["regression"],
        //     nDocs: nDocs,
        //     docs: function(i) {
        //         return {a: i};
        //     },
        //     op: {op: "find", query: {a: {$lte: nDocs}}},
        //     createViewsPassthrough: false,
        //     createAggregationTest: false
        // });
        let r = Math.random();
        if (r <= 1/3) {
            testCaseBaseline();
        } else if (r <= 2/3) {
            testCaseAppendOnly();
        } else {
            testCaseExperiment();
        }
    }

}());
