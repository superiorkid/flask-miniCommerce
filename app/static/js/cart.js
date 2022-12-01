const addToCart = (productId) => {
  fetch(`http://127.0.0.1:5000/cart/${productId}/add`, {
    method: "POST",
  }).then((res) => {
    if (!res.ok) {
      throw new Error("unsuccessfull add product to cart.");
    }
  });

  location.reload();
};

const removeFromCart = (productId) => {
  fetch(`http://127.0.0.1:5000/cart/${productId}/remove`, {
    method: "DELETE",
  });

  location.reload();
};
