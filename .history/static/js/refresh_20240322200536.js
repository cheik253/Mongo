
        // Get the session timeout value in seconds from Flask
        var sessionTimeoutSeconds = {{ session_timeout_seconds }};
        
        // Convert session timeout to milliseconds
        var sessionTimeoutMilliseconds = sessionTimeoutSeconds * 1000;

        // Function to reload the page after session timeout
        function reloadPageAfterSessionTimeout() {
            setTimeout(function() {
                location.reload(true); // Reload the page
            }, sessionTimeoutMilliseconds);
        }

        // Call the function to start the countdown
        reloadPageAfterSessionTimeout();
    </script>