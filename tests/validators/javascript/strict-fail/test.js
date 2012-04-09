/* Fail something which should fail in strict mode */

/*global window*/

(function() {
    function foobar() {
        if(window.foobar == 0) {
            // Should use === to compare with 0
            foobar();
        }
    }
})();