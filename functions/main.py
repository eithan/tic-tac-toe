import functions_framework

@functions_framework.http
def main(request):
    """HTTP Cloud Function entry point."""
    return {"message": "Hello from Firebase!", "status": "success"}
