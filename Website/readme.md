# Gemini_Survey Website

This project is a survey website utilizing the Gemini API. Follow the instructions below to set up and run the project on your local machine.

## Prerequisites

- Python 3.7 or higher
- Git

## Getting Started

1. **Clone the repository**

    ```sh
    git clone https://github.com/Aaryanpanthi/Gemini_Survey.git
    cd Gemini_Survey/Website
    ```

2. **Create a virtual environment**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**

    - On macOS and Linux:

        ```sh
        source venv/bin/activate
        ```

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

4. **Install the required packages**

    ```sh
    pip install -r requirements.txt
    ```

5. **Configure the API Key**

    Open `main.py` and input your API key in the following line:

    ```python
    genai.configure(api_key='Your_API_Key')
    ```

6. **Run the Streamlit app**

    ```sh
    streamlit run main.py --server.enableCORS=false
    ```

## Usage

Once the app is running, you can access it in your web browser at `http://localhost:8501`.

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
