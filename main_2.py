from Deployment import create_app

app = create_app()

if __name__ == '__main__':
    print("Starting Zamboanga Del Norte Economic Analytics & Advisory Server (main_2)...")
    app.run(host='0.0.0.0', port=5000, debug=True)
