# Restful EasyOCR

If you do not know, EasyOCR is an open-sourced project (written in Python, hosted at https://github.com/JaidedAI/EasyOCR) helps doing OCR Jobs for your text extraction needs. Because it's written in Python, it can be difficult for integrating to your stack. 

This small repository helps wrapping the EasyOCR functionalities inside Restful API with Flask. So that, you do not need to use Python in your stack to work with EasyOCR.

### HTTP Request:

- Method: `POST`

- URL: `http://{server-ip}:8080/ocr`

- Header: 

  - Content-Type: application/json

- Request Body:

  - JSON Object with format:

    - `image_url` - (String) : URL Of image will be processed
    - `secret_key` - (String): Secret Key of server. If you're using my public image from hub.docker.com, the secret key will be "easyocr_vdt". Change this key by set the value of environment variable `SECRET_KEY` in `docker run...` command.

  - Example of a payload:

    ```
    {
    	"secret_key": "easyocr_vdt",
    	"image_url": "https://via.placeholder.com/300.jpg?text=Hello_world"
    }
    ```

    *(Placeholder Image above has resolution 300x300px)*

### HTTP Response:
- Status Code: `200` (Success) or `401` if incorrect `secret_key`.

- Format: JSON

  - `results` (Array of Object): List of detected texts and rectangle boundary of that text on the source image. Each result object will have format:

    - `coordinate` (Array of Point): Contains 4 points to create rectangle contains the text. Each point is an two value array of float.
    - `score` (Float): The score of the easyocr when detect. From 0 (zero) to 1.
    - `text` (String): Detected text

  - An Example of response data: 

    ```json
    {
      "results": [
        {
          "coordinate": [
            [
              86.0,
              138.0
            ],
            [
              212.0,
              138.0
            ],
            [
              212.0,
              170.0
            ],
            [
              86.0,
              170.0
            ]
          ],
          "score": 0.24089430272579193,
          "text": "Hello world"
        }
      ]
    }
    ```

 