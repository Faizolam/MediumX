from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import FileResponse
import shutil
import os
from datetime import datetime
from sqlalchemy import func
# from ..models.postModel import Post
from ..models import postModel, likeModel
from ..schemas import postSchemas
from ..modelsOperaions.post import PostOpration
from ..core.database import get_db, engine
from ..import oauth2

postModel.Base.metadata.create_all(bind=engine) # This line creates the tables in the database based on the SQLAlchemy models defined in postModel. It uses the metadata from the Base class to generate the necessary SQL commands to create the tables if they do not already exist. The bind=engine argument specifies the database connection to use for executing the commands. This is typically done at the application startup to ensure that the database schema is in place before handling any requests.

# APIRouter is a class provided by FastAPI that allows you to create modular and reusable route groups. It helps in organizing your API endpoints into logical sections, making your code cleaner and more maintainable. You can define a set of routes under a common prefix and tag them for better documentation in the API docs. In this code, we are creating a router for all post-related endpoints, which will be prefixed with "/posts" and tagged as "Posts" for documentation purposes.
router = APIRouter(
    prefix="/posts", # All routes start with /posts
    tags=['Posts'] # This is used for documentation purposes to group related endpoints together in the API docs.
)


@router.get("/", status_code=status.HTTP_200_OK, response_model= List[postSchemas.PostWithLikes])
# @router.get("/", status_code=status.HTTP_200_OK)
def get_posts(db : Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """
    Retrieve all posts with pagination and search functionality.
    
    This endpoint retrieves a list of all posts from the database with optional
    filtering by search term and pagination support.
    
    Args:
        db (Session): Database session dependency for querying posts.
        limit (int, optional): Maximum number of posts to return. Defaults to 10.
        skip (int, optional): Number of posts to skip for pagination. Defaults to 0.
        search (str, optional): Search term to filter posts. Defaults to empty string.
    
    Returns:
        List[PostWithLikes]: A list of posts with their associated likes.
    
    Status Codes:
        200: Posts retrieved successfully.
    """

    posts = PostOpration(db).get_post(limit=limit, skip=skip, search=search)
    return posts

@router.get("/display/{filename}",status_code=status.HTTP_200_OK)
async def download_file(filename: str):
    """
    Retrieve and display an image file by filename.
    
    This endpoint serves image files that have been uploaded for posts.
    The file is retrieved from the Upload/images directory and returned
    as a JPEG image response.
    
    Args:
        filename (str): The name of the image file to retrieve.
    
    Returns:
        FileResponse: The image file if found, or error message if not found.
    
    Status Codes:
        200: Image file retrieved successfully.
        404: Image file not found (returned as JSON error).
    
    Notes:
        - Files are stored in the ./Upload/images/ directory.
        - Only JPEG format is currently supported.
    """
    file_path = f"./Upload/images/{filename}"  # Replace with the actual directory
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpeg")
    return {"error": "File not found"}

@router.get("/ofsingaluser", status_code=status.HTTP_200_OK, response_model=List[postSchemas.PostRead])
def get_own_posts(db:Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    """
    Retrieve all posts created by the authenticated user.
    
    This endpoint returns a list of all posts owned by the currently authenticated user.
    Authentication is required to access this endpoint.
    
    Args:
        db (Session): Database session dependency for querying posts.
        current_user (int): The ID of the currently authenticated user (injected by oauth2).
    
    Returns:
        List[PostRead]: A list of posts created by the authenticated user.
    
    Raises:
        HTTPException: If the user is not authenticated (401 Unauthorized).
    
    Status Codes:
        200: User's posts retrieved successfully.
        401: Authentication required or invalid token.
    """

    posts = PostOpration(db).own_posts(owner_id=current_user.id)
    print(posts)
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=postSchemas.PostWithLikes)
def get_post_id(id: int, db : Session = Depends(get_db)):
    """
    Retrieve a single post by its ID.
    
    This endpoint fetches a specific post from the database using its unique identifier.
    The response includes the post details along with associated likes.
    
    Args:
        id (int): The unique identifier of the post to retrieve.
        db (Session): Database session dependency for querying posts.
    
    Returns:
        PostWithLikes: The post object with its associated likes.
    
    Raises:
        HTTPException: If the post with the specified ID does not exist (404 Not Found).
    
    Status Codes:
        200: Post retrieved successfully.
        404: Post not found.
    """

    single_post =  PostOpration(db).get_post_by_id(post_id=id)
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return single_post
    
    

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=postSchemas.PostRead)
def create_posts(post_data: postSchemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Create a new post for the authenticated user.
    
    This endpoint creates a new blog post with the provided data and associates it
    with the currently authenticated user as the owner. Authentication is required.
    
    Args:
        post_data (PostCreate): The post data including title, content, and metadata.
        db (Session): Database session dependency for persisting the post.
        current_user (int): The ID of the currently authenticated user (injected by oauth2).
    
    Returns:
        PostRead: The created post object with its ID and metadata.
    
    Raises:
        HTTPException: If the user is not authenticated (401 Unauthorized).
    
    Status Codes:
        201: Post created successfully.
        401: Authentication required or invalid token.
    
    Notes:
        - The owner_id of the post is automatically set to the current user's ID.
    """

    print(current_user.id)
    postOpt = PostOpration(db)
    newPost = postOpt.get_create_post(owner_id =current_user.id, post_data=post_data)
    # post_img = upload_image(UploadFile = File(...))
    return newPost

@router.post("/upload-image", status_code=status.HTTP_200_OK)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image file for use in posts.
    
    This endpoint handles image file uploads and stores them in the Upload/images
    directory with a unique filename based on the current timestamp to avoid conflicts.
    The original file extension is preserved.
    
    Args:
        file (UploadFile): The image file to upload (form-data file input).
    
    Returns:
        dict: A dictionary containing:
            - filename (str): The generated unique filename.
            - status (str): Upload status message.
            - content (int): Number of bytes written.
            Or an error dictionary if upload fails.
    
    Raises:
        Exception: Any file I/O or processing errors are caught and returned as error.
    
    Status Codes:
        200: Image uploaded successfully.
    
    Notes:
        - Filenames are generated using current timestamp to ensure uniqueness.
        - Original file extension is preserved.
        - Files are stored in Upload/images/ directory relative to app root.
    """
    try:
        uniqueFileName=str(datetime.now().timestamp()).replace(".","")
        print(uniqueFileName)
        fileNamesplit=str(file.filename).split(".")
        print(fileNamesplit)

        ext = fileNamesplit[len(fileNamesplit)-1]
        finalFileName=f"{uniqueFileName}.{ext}"
        finalFilePath=f"Upload/images/{finalFileName}"

        os.makedirs("Upload/images/",exist_ok=True)

        with open(finalFilePath, "wb")as buffer:
            content = await file.read()
            res=buffer.write(content)

    except Exception as e:
        return {"error": str(e)}
    
    return {"filename": finalFileName, "status":"Image uploaded Successfully","content":res}


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=postSchemas.PostRead)
def update_post(id:int, updated_data:postSchemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Update an existing post by its ID.
    
    This endpoint allows authenticated users to update their own posts. Users can only
    modify posts they own. Authorization is enforced by verifying the owner_id matches
    the current user.
    
    Args:
        id (int): The unique identifier of the post to update.
        updated_data (PostUpdate): The updated post data (fields to be modified).
        db (Session): Database session dependency for updating the post.
        current_user (int): The ID of the currently authenticated user (injected by oauth2).
    
    Returns:
        PostRead: The updated post object.
    
    Raises:
        HTTPException: 
            - 404 Not Found: If the post does not exist.
            - 403 Forbidden: If the user is not the owner of the post.
            - 401 Unauthorized: If the user is not authenticated.
    
    Status Codes:
        200: Post updated successfully.
        401: Authentication required or invalid token.
        403: User is not authorized to update this post.
        404: Post not found.
    """

    print(current_user)
    postOpt= PostOpration(db)
    updated_post = postOpt.get_update_post(post_id=id, update_post=updated_data)
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requsted action")
    return updated_post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Delete a post by its ID.
    
    This endpoint allows authenticated users to delete their own posts. Users can only
    delete posts they own. Authorization is enforced by verifying the owner_id matches
    the current user. The associated likes and comments will be cascade-deleted.
    
    Args:
        id (int): The unique identifier of the post to delete.
        db (Session): Database session dependency for deleting the post.
        current_user (int): The ID of the currently authenticated user (injected by oauth2).
    
    Returns:
        Response: HTTP 204 No Content response on successful deletion.
    
    Raises:
        HTTPException:
            - 404 Not Found: If the post does not exist.
            - 403 Forbidden: If the user is not the owner of the post.
            - 401 Unauthorized: If the user is not authenticated.
    
    Status Codes:
        204: Post deleted successfully (No Content).
        401: Authentication required or invalid token.
        403: User is not authorized to delete this post.
        404: Post not found.
    
    Notes:
        - This is a destructive operation and cannot be undone.
        - All associated likes and comments are also deleted.
    """

    print(current_user)
    postOpt = PostOpration(db)
    del_post = postOpt.get_delete_post(post_id=id)

    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requestd action")
    
    postOpt.get_delete(del_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) 