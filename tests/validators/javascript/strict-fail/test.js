/* Fail something which should fail in strict mode */

function foobar() {
	var i;

	for(i=0; i<100; i++) {
		function foobar2() {
			// Function created inside loop
		}
	}
}