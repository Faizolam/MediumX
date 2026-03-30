from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post,user,auth,like,comment



app = FastAPI()


origins = ["*"]
# The allow_origins parameter is set to ["*"], which means that requests from any origin will be allowed. This is useful during development or when you want to allow access from multiple domains, but in a production environment, you should specify the allowed origins more restrictively for security reasons.

# The allow_credentials parameter is set to True, which allows cookies and authentication credentials to be included in cross-origin requests. This is important if your frontend needs to send cookies or use authentication when making requests to the backend.

# The allow_methods parameter is set to ["*"], which means that all HTTP methods (GET, POST, PUT, DELETE, etc.) are allowed in cross-origin requests. You can specify specific methods if you want to restrict the types of requests that can be made.

# The allow_headers parameter is set to ["*"], which means that all headers are allowed in cross-origin requests. You can specify specific headers if you want to restrict the types of headers that can be included in requests.Eg: if your frontend only needs to send certain headers, you can specify them here for better security.

# Overall, this configuration allows for a very permissive CORS policy, which can be useful during development but should be tightened in production to enhance security.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# The include_router method is used to include the routers defined in the auth, user, post, like, and comment modules. Each router contains the endpoints related to its respective functionality (e.g., authentication, user management, post management, etc.). By including these routers in the main FastAPI application, you can organize your code into modular components and keep your main application file clean and manageable. Each router will handle specific routes and logic related to its functionality, making it easier to maintain and scale your application as it grows.
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(like.router)
app.include_router(comment.router)

@app.get("/")
def root():
    return {"message": "Bismallah, Let's Build a Blogging Web"}

# The request_path is /healthz, which should be an HTTP endpoint in your Cloud Run service.
# The health check will send HTTP requests to this path to verify if the service is running and healthy.
@app.get("/healthz")
def health_check():
    return{"status":"healthy"}

# Manually test the /healthz endpoint by deploying the service and checking the response from a browser or using tools like curl
# curl https://<cloud-run-service-url>/healthz

#~ how do you handle versioning in large APIs?
# In large APIs, versioning is typically handled by including the version number in the URL path. For example, you might have endpoints like /api/v1/posts and /api/v2/posts. This allows you to make changes to the API without breaking existing clients that rely on the older version. You can also use query parameters or headers for versioning, but URL path versioning is more common and easier to manage in large APIs. 

#~ How do you implement rate limiting in a FastAPI application?
# To implement rate limiting in a FastAPI application, you can use middleware or third-party libraries such as `slowapi` or `fastapi-limiter`. These libraries allow you to define rate limits for your endpoints, such as limiting the number of requests per minute from a single IP address. You can configure the rate limits based on your application's needs and apply them to specific routes or globally across the entire application. This helps prevent abuse and ensures that your API remains responsive under heavy load.
# Eg:
# from slowapi import Limiter  
# from slowapi.util import get_remote_address   
# limiter = Limiter(key_func=get_remote_address)
# app = FastAPI()  
# app.state.limiter = limiter
# app.add_exception_handler(429, limiter._rate_limit_exceeded_handler)
# @app.get("/some-endpoint")
# @limiter.limit("5/minute")   
# async def some_endpoint():
#     return {"message": "This endpoint is rate limited to 5 requests per minute." }
# In this example, the `slowapi` library is used to create a rate limiter that limits requests to 5 per minute for the specified endpoint. You can adjust the rate limit as needed and apply it to different endpoints in your FastAPI application. 

# How do you rate limit by user instead of by IP address?
# To rate limit by user instead of by IP address, you can modify the key function used by the rate limiter to identify users based on their authentication credentials rather than their IP address. For example, if you are using JWT tokens for authentication, you can extract the user ID from the token and use it as the key for rate limiting. Here's an example using `slowapi`:
# from slowapi import Limiter
# from slowapi.util import get_remote_address
# def get_user_id(request):
#     # Extract user ID from the request (e.g., from JWT token)
#     user_id = extract_user_id_from_token(request)
#     return user_id
# limiter = Limiter(key_func=get_user_id)
# app = FastAPI()
# app.state.limiter = limiter
# app.add_exception_handler(429, limiter._rate_limit_exceeded_handler)
# @app.get("/some-endpoint")
# @limiter.limit("5/minute")
# async def some_endpoint():
#     return {"message": "This endpoint is rate limited to 5 requests per minute per user."}
# In this example, the `get_user_id` function is defined to extract the user ID from the request, and it is used as the key function for the rate limiter. This way, the rate limit will be applied based on the user making the request rather than their IP address. Each user will have their own separate rate limit, allowing for more granular control over API usage.    