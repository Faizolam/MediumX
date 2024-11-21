let BASE_URL = `http://127.0.0.1:8000/`;

function getPostIdFromUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("id");
}
// let postId = 29;
async function getPostsById(postId) {
  try {
    let response = await fetch(`${BASE_URL}posts/${postId}`);
    if (response.ok) {
      let postData = await response.json();
      // console.log("Post Data:", postData);
      displayPostContent(postData);
      countClicks(postId, postData.likes);
      commentData(postId);
      getComments(postId);
    } else {
      console.error("Error fetching post: ", response.status);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

function displayPostContent(postData) {
  // if(!postData || !postData.PostRead){
  //     console.log("Post data or PostRead is undefined");
  //     return;
  // }
  const post = postData.PostRead;
  const likes = postData.likes;
  const noComment = postData.noComment || 0;

  const postTitle = document.querySelector(".post-title");
  const postSummary = document.getElementById("post-summry");
  const postAuthor = document.getElementById("post-author");
  const postDate = document.getElementById("post-date");
  const noLikes = document.querySelector(".no-likes span");
  const noComments = document.querySelector(".no-commnet span");
  const postImage = document.querySelector(".head-img img"); // Image element
  const postContent = document.querySelector(".blog-content p");

  postTitle.textContent = post.title;
  postSummary.textContent = post.summary;
  postAuthor.textContent = `By ${post.user.username} .`;
  noLikes.textContent = likes;
  noComments.textContent = noComment;
  postContent.textContent = post.content;
  postDate.textContent = new Date(post.created_at).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  if(post.image_post){
    getImagePost(post.image_post, postImage);
    // console.log("DPC",getImagePost(post.image_post, postImage))
  }

}

const postId = getPostIdFromUrl();

// console.log(typeof(Number(postId)));
if (postId) {
  getPostsById(postId);
  // countClicks(postId);
  // let data = getPostsById(postId)
  // console.log(data)
} else {
  console.error("Error: No post ID found in URL.");
}

//get posts list
async function getPosts() {
  try {
    let response = await fetch(`${BASE_URL}posts/`);
    if (response.ok) {
      let posts = await response.json();
      displayPosts(posts);
    } else {
      console.error("Error fetching posts:", response.status);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

function displayPosts(posts) {
  const postsContainer = document.getElementById("posts-container");
  postsContainer.innerHTML = "";

  posts.forEach((postData) => {
    const post = postData.PostRead;
    const likes = postData.likes;
    const noComment = postData.noComment || 0;
    const formattedDate = new Date(post.created_at).toLocaleDateString(
      "en-US",
      {
        year: "numeric",
        month: "short",
        day: "numeric",
      }
    );

    // Generate post HTML structure
    const postHTML = `
            <div class="home-article blog-home-article">
                <a href="/blog.html?id=${post.id}">
                <div class="home-article-img blog-home-article-img">
                    <img id="post-img-${post.id}" src="img/shubham-dhage.jpg" alt="article" />
                </div>
                <div class="home-article-content blog-home-article-content">
                    <span id="author">${post.user.username}</span>
                    <a href="/blog.html?id=${post.id}">
                        <h2>${post.title}</h2>
                        <h3>${post.summary}</h3>
                    </a>
                    <a href="/blog.html?id=${post.id}">
                        <div class="meta">
                            <span>${formattedDate}</span>
                            <div class="likes">
                                <img src="svg/like.svg" alt="" srcset="" />
                                <button class="n"><span>${likes}</span></button>
                            </div>
                            <div class="comments">
                                <button class="ind-commBtn" aria-label="responses">
                                    <img src="svg/comment.svg" alt="" srcset="" />
                                </button>
                                <button class="n"><span>${noComment}</span></button>
                            </div>
                        </div>
                    </a>
                </div></a>
        </div>
        `;
    postsContainer.innerHTML += postHTML;

     // Fetch and set the image dynamically for each post
    const imgElement = document.getElementById(`post-img-${post.id}`)
    // console.log(imgElement)
    if(post.image_post){
      // console.log(post.image_post)
      // let filename=post.image_post
      getImagePost(post.image_post, imgElement);
    }

  });
}
getPosts();


async function getImagePost(filename, imgElement = null) {
  try {
    let response = await fetch(`${BASE_URL}posts/display/${filename}`);
    if (response.ok) {
      let imgBlob = await response.blob(); // Fetch the image as a blob
      let imgUrl = URL.createObjectURL(imgBlob); // Create a URL for the blob
      // console.log(imgBlob)

      if (imgElement) {
        // Dynamically set the image source if an element is provided
        imgElement.src = imgUrl;
        imgElement.alt = "Post Image";
      } else {
        // Return the image URL for other uses
        return imgUrl;
      }
    } else {
      console.error("Error fetching image: ", response.status);
    }
  } catch (error) {
    console.error("Error fetching image:", error.message);
  }
}




function toggleComment() {
  const commentBox = document.getElementById("comments-box");

  if (commentBox.classList.contains("open")) {
    commentBox.classList.remove("open");
    commentBox.classList.add("closed");
    console.log(commentBox.classList);
  } else {
    commentBox.classList.remove("closed");
    commentBox.classList.add("open");
    console.log(commentBox.classList);
  }
}

const closeBtn = document.getElementById("closebtn");
const commentBox = document.getElementById("comments-box");
closeBtn.addEventListener("click", function () {
  commentBox.classList.add("closed");
  commentBox.classList.remove("open");
});

// const greenButton = document.getElementById('res');

// greenButton.addEventListener('click', () => {
//   greenButton.classList.toggle('clicked');
// });

async function countClicks(postId, likes) {
  const likeBtn = document.getElementById("like");
  let clicked = likes;

  likeBtn.addEventListener("click", async function () {
    clicked = clicked === 0 ? 1 : 0;
    console.log("Clicked status:", clicked);

    await updateLikesCount(postId);
    await userLike(postId, clicked);
  });
}

async function userLike(postId, clicked) {
  const token = localStorage.getItem("accessToken");
  console.log("Access Token:", token);

  try {
    let response = await fetch(`${BASE_URL}like`, {
      method: "POST",
      body: JSON.stringify({
        post_id: postId,
        dir: clicked,
      }),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      let userLikeRes = await response.json();
      console.log("User Like Response: ", userLikeRes);
    } else {
      console.error("Error fetching user like, status: ", response.status);
    }
  } catch (error) {
    console.error("Request failed:", error);
  }
}

async function updateLikesCount(postId) {
  try {
    let response = await fetch(`${BASE_URL}posts/${postId}`);
    if (response.ok) {
      let postData = await response.json();
      const updatedLikes = postData.likes;

      const noLikes = document.querySelector(".no-likes span");
      if (noLikes) {
        noLikes.textContent = updatedLikes;
      } else {
        console.error("Likes element not found in the DOM.");
      }
    } else {
      console.error("Error fetching updated likes:", response.status);
    }
  } catch (error) {
    console.error("Error fetching post data:", error);
  }
}
//functions to heandel comments

// const cancelBtn = document.getElementById("cl");
// const commentTxt = document.getElementById("comt-txt span");
// console.log(commentTxt)
// cancelBtn.addEventListener('click', function(){

// })

const cancelButton = document.querySelector(".cl");
const responseButton = document.querySelector(".res");
const inputField = document.querySelector(".comt-txt input");

cancelButton.addEventListener("click", () => {
  inputField.value = "";
});

function commentData(postId) {
  const responseButton = document.querySelector(".res");
  const inputField = document.querySelector(".comt-txt input");

  responseButton.addEventListener("click", async () => {
    const content = inputField.value;
    await createComment(content, postId);
  });
}

async function createComment(content, postId) {
  const token = localStorage.getItem("accessToken");
  console.log(content, postId);

  try {
    let response = await fetch(`${BASE_URL}comment/${postId}`, {
      method: "POST",
      body: JSON.stringify({
        comment: content,
      }),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      let userComment = response.json();
      inputField.value = "";
      console.log("user's comment:", userComment);
    } else {
      console.error("getting error while creating comment", response.status);
    }
  } catch (error) {
    console.error("Error fetching post data:", error);
  }
}

async function getComments(postId) {
  try {
    let response = await fetch(`${BASE_URL}comment/${postId}`);
    if (response.ok) {
      let comments = await response.json();
      // console.log(comments);
      displayComment(comments);
    } else {
      console.error("Error fetching comments", response.status);
    }
  } catch (error) {
    console.error("error", error);
  }
}

function displayComment(comments) {
  const commentMainContainer = document.getElementById(
    "comment-main-container"
  );
  commentMainContainer.innerHTML = "";

  comments.forEach((commentContent) => {
    const comment = commentContent.comment;
    const comment_date = commentContent.comment_date;
    const username = commentContent.user.username;
    formattedComDate = new Date(comment_date).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
    // console.log(username)

    commentHTML = `
        <div class="comment-container">
                <div class="user-info">
                <div class="comment-user">
                    <img alt="" src="https://miro.medium.com/v2/resize:fill:40:40/1*dmbNkD5D-u45r44go_cf0g.png" width="32" height="32" loading="lazy">
                    <span>${username}</span>
                    <span>${formattedComDate}</span>
                </div>
                <div class="l"></div>
                </div>
                <div class="comment-text" id="comt-txt">
                <p><span>${comment}</span></p>
                </div>
                <div>
                <div class="comment-like">
                    <div class="likes">
                    <button class="n" id="like"><img src="svg/like.svg"/></button>
                    <button class="no-likes n"><span>0</span></button>
                    </div>
                    <div class="comments align-l">
                    <button class="comments-btn">
                        <img src="svg/comment.svg"/>
                    </button>
                    <button class="no-commnet n"><span>0</span></button>
                    </div>
                    <div class="reply">...</div>
                </div>
                </div>
        </div>`;
        commentMainContainer.innerHTML += commentHTML;
  });
}