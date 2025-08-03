import os
import shutil
import tempfile
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def copy_edge_profile():
    """Copies the default Edge user profile to a temporary directory, ignoring locked files."""
    username = os.environ.get("USERNAME")
    original_profile = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default"
    temp_dir = tempfile.mkdtemp()
    temp_profile = os.path.join(temp_dir, "EdgeProfile", "Default")

    print(f"[*] Copying Edge profile (excluding locked folders) to {temp_profile}...")

    def ignore_locked_files(src, names):
        ignored = []
        for name in names:
            path = os.path.join(src, name)
            try:
                with open(path, "rb"):
                    pass
            except:
                ignored.append(name)
        return ignored

    try:
        shutil.copytree(original_profile, temp_profile, ignore=ignore_locked_files, dirs_exist_ok=True)
    except Exception as e:
        print(f"[!] Failed to copy some files: {e}")

    return os.path.join(temp_dir, "EdgeProfile"), temp_dir


def navigate_to_url(page, url):
    """Navigates to the given URL and waits for the page to load completely."""
    print("[*] Navigating to the URL and waiting for page load...")

    with page.expect_response(lambda r: r.url.startswith(url)) as response_info:
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle", timeout=60000)

    response = response_info.value
    print(f"[✓] HTTP status code: {response.status}")
    if response.status >= 400:
        print(f"[!] ⚠ Page returned error status code: {response.status}")

    return response


def take_screenshot(page, filename="final_screenshot.png"):
    """Takes a screenshot of the current page."""
    try:
        page.screenshot(path=filename)
        print(f"[✓] Screenshot saved as '{filename}'")
    except Exception as e:
        print(f"[!] Failed to take screenshot: {e}")


def run_generic_checks(page):
    """Performs generic sanity checks on the loaded page."""
    print("[*] Running generic checks...")

    try:
        body_text = page.inner_text("body").strip()
        word_count = len(body_text.split())

        if word_count < 20:
            print(f"[!] ⚠ Low word count ({word_count}). Page might not be fully loaded.")
        else:
            print(f"[✓] Page text word count: {word_count}")

        selectors = [
            "button", "input[type='button']", "input[type='submit']",
            "[role='button']", "[class*='btn']", "[class*='button']"
        ]

        button_present = any(page.query_selector(sel) for sel in selectors)
        input_present = page.query_selector("input") is not None
        link_present = page.query_selector("a") is not None

        print("[✓] Input field detected." if input_present else "[✗] No input field found.")
        print("[✓] Button element detected." if button_present else "[✗] No button element found.")
        print("[✓] Link element detected." if link_present else "[✗] No link element found.")

        soup = BeautifulSoup(page.content(), "html.parser")
        tag_types = set(tag.name for tag in soup.find_all())

        if len(tag_types) < 5:
            print(f"[!] ⚠ Very few HTML tag types detected ({len(tag_types)}). Page may be broken.")
        else:
            print(f"[✓] Page has {len(tag_types)} unique tag types — DOM structure seems OK.")
    except Exception as e:
        print(f"[!] Failed during generic checks: {e}")


def check_console_errors(page):
    """Captures and reports JavaScript console errors."""
    print("[*] Checking for JavaScript console errors...")
    errors = []

    def handle_console(msg):
        if msg.type == "error":
            errors.append(msg.text)

    try:
        page.on("console", handle_console)
        page.evaluate("console.clear()")
        page.wait_for_timeout(5000)

        if errors:
            print(f"[!] {len(errors)} JavaScript console error(s) detected:")
            for err in errors:
                print(f"    ⚠ {err}")
        else:
            print("[✓] No JavaScript console errors detected.")
    except Exception as e:
        print(f"[!] Failed to check console errors: {e}")


def analyze_page(page):
    """Performs all page diagnostics."""
    print(f"[+] Final URL: {page.url}")
    print(f"[+] Page Title: {page.title()}")
    take_screenshot(page)
    run_generic_checks(page)
    check_console_errors(page)


def cleanup_temp_profile(temp_dir):
    """Deletes the temporary profile directory."""
    print("[*] Cleaning up temp profile...")
    shutil.rmtree(temp_dir, ignore_errors=True)
    print("[✓] Temp profile deleted successfully.")


def launch_and_test_url(url):
    """Main function to copy profile, launch browser, navigate to URL, and perform diagnostics."""
    profile_path, temp_dir = copy_edge_profile()

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=profile_path,
                headless=False,
                channel="msedge",
                args=["--no-first-run", "--ignore-certificate-errors"]
            )
            page = browser.pages[0] if browser.pages else browser.new_page()

            navigate_to_url(page, url)
            analyze_page(page)

            input("Press Enter to close browser...")
            browser.close()

    except Exception as e:
        print(f"[!] Error: {e}")

    finally:
        cleanup_temp_profile(temp_dir)


if __name__ == "__main__":
    import sys
    test_url = sys.argv[1] if len(sys.argv) > 1 else input("Enter the internal app URL to test: ").strip()
    launch_and_test_url(test_url)
