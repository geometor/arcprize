from playwright.sync_api import sync_playwright

# HTML content with a simple CSS animation and a timer
html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @keyframes move {
            0% { transform: translateX(0); }
            100% { transform: translateX(200px); }
        }
        .box {
            width: 50px;
            height: 50px;
            background-color: red;
            animation: move 2s infinite alternate;
        }
        #timer {
            font-size: 24px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="box"></div>
    <div id="timer">0.00</div>
    <script>
        let startTime = Date.now();
        let timerElement = document.getElementById('timer');
        function updateTimer() {
            let elapsedTime = (Date.now() - startTime) / 1000;
            timerElement.textContent = elapsedTime.toFixed(2);
            if (elapsedTime < 10) {
                requestAnimationFrame(updateTimer);
            }
        }
        updateTimer();
    </script>
</body>
</html>
"""

def capture_animation_with_timer():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Start video recording
        context = browser.new_context(
            record_video_dir="./videos/",
            record_video_size={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        
        # Set the content of the page directly
        page.set_content(html_content)
        # Wait for the timer to reach 5 seconds
        page.wait_for_function("() => parseFloat(document.getElementById('timer').textContent) >= 5")
        
        # Close the context to stop recording
        context.close()
        # Retrieve the path to the recorded video
        video_path = page.video.path()

        # Close the browser
        browser.close()

    print("Video captured as", video_path)

if __name__ == "__main__":
    capture_animation_with_timer()

