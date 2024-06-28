
// (function (){
// window.history.pushState(null, '', window.location.href);

// // Listen for the back button click event
// window.addEventListener('popstate', function(event) {
//     // Redirect the user to the page before the update page
//     window.location.href = '/index/';
// });
// })();

(function () {
    // Replace the current state in the browser history
    history.replaceState(null, null, location.href);

    // Disable the back button
    history.pushState(null, null, location.href);
    window.onpopstate = function () {
        history.go(1);
    };
})();
