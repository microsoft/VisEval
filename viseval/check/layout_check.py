import os
import uuid

overflowScript = """const isElementOutsideCanvas = (element) => {
    // Get the bounding box of the SVG element
    let svgRect = element.getBBox();

    // Get the viewBox attribute of the SVG element
    let svgElement = document.querySelector('svg');
    let viewBoxValue = svgElement.getAttribute('viewBox');
    let viewBoxArray = viewBoxValue.split(' ').map(Number);
    let minX = viewBoxArray[0];
    let minY = viewBoxArray[1];
    let width = viewBoxArray[2];
    let height = viewBoxArray[3];

    // Check if any part of the element is outside the canvas
    if (svgRect.x < minX || svgRect.y < minY || svgRect.x + svgRect.width > width+minX || svgRect.y + svgRect.height > height+minY) {
        return true;
    } else {
        return false;
    }
}

let svgElement = document.querySelector('#axes_1');
return isElementOutsideCanvas(svgElement);
"""

overlapScript = """const isTextOverlap = (parentElement) => {
    let index = 1;
    let flag = true;
    let textArray = [];
    while (flag) {
        let textElement = parentElement.querySelector('#text_' + index);
        if (textElement) {
            index++;
            let gElement = textElement.querySelector('g');
            let transform = gElement.getAttribute('transform');
            if (transform) {
                const rotateMatch = transform.match(/rotate\(([^)]+)\)/);
                let notRotate = true;
                if (rotateMatch) {
                    const rotateValue = parseFloat(rotateMatch[1]) % 90;
                    if (Math.abs(rotateValue) > 10 && Math.abs(rotateValue) < 80) {
                        notRotate = false;
                    }
                }

                if (notRotate) {
                    let bbox = textElement.getBBox();
                    textArray.push(bbox);
                }
            }
        }
        else {
            flag = false;
        }
    }
    let textOverlap = false;
    let textArrayLength = textArray.length;
    for (let i = 0; i < textArrayLength; i++) {
        for (let j = i + 1; j < textArrayLength; j++) {
            let text1Rect = textArray[i];
            let text2Rect = textArray[j];
            if (text1Rect.x < text2Rect.x + text2Rect.width &&
                text1Rect.x + text1Rect.width > text2Rect.x &&
                text1Rect.y < text2Rect.y + text2Rect.height &&
                text1Rect.y + text1Rect.height > text2Rect.y) {
                textOverlap = true;
                break;
            }
        }
    }
    return textOverlap;
}

let svgElement = document.querySelector('#axes_1');
return isTextOverlap(svgElement)
"""


def layout_check(context: dict, webdriver_path):
    svg_string = context["svg_string"]

    if webdriver_path is not None:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service

        # Chrome headless mode
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        try:
            service = Service(webdriver_path)
            webdriver = webdriver.Chrome(service=service, options=options)

            current_directory = os.getcwd()
            file_path = f"{current_directory}/temp_{uuid.uuid1()}.svg"

            with open(file_path, "w") as svg_file:
                svg_file.write(svg_string)

            webdriver.get(f"file://{file_path}")
            overflow_result = not webdriver.execute_script(overflowScript)
            overlap_result = not webdriver.execute_script(overlapScript)
            webdriver.close()
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Remove file error: {e}")

            if overflow_result and overlap_result:
                msg = "No overflow or overlap detected."
            elif not overflow_result and not overlap_result:
                msg = "Overflow and overlap detected."
            elif not overflow_result:
                msg = "Overflow detected."
            else:
                msg = "Overlap detected."
            return overflow_result and overlap_result, msg
        except Exception as e:
            print(e)

    return None, "No webdriver path provided."
