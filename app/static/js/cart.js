const addToCart = (productId) => {
  fetch(`http://127.0.0.1:5000/cart/${productId}/add`, {
    method: "POST",
  }).then((res) => {
    if (!res.ok) {
      throw new Error("unsuccessfull add product to cart.");
    }

    alert("Product added to cart.");
  });

  location.reload();
};

const removeFromCart = (productId) => {
  fetch(`http://127.0.0.1:5000/cart/${productId}/remove`, {
    method: "DELETE",
  });
  alert("Product remove from cart.");
  location.reload();
};

const product_checkout = () => {
  let product = document.getElementsByClassName("product");
  let product_name = document.getElementsByClassName("name");
  let price = document.getElementsByClassName("price");
  let quantity = document.getElementsByClassName("quantity");
  let cost = document.getElementsByClassName("cost");
  let total = document.getElementById("total");

  let carts = [];

  for (let i = 0; i < product.length; i++) {
    let cart = {
      name: product_name[i].innerHTML,
      price: price[i].innerHTML,
      quantity: quantity[i].value,
      cost: cost[i].innerHTML,
      total: total.innerHTML,
    };
    carts.push(cart);
  }

  fetch(`http://127.0.0.1:5000/checkout`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(carts),
    headers: new Headers({
      "content-type": "application/json",
    }),
  }).then((response) => {
    if (response.redirected) {
      window.location = response.url;
    }
  });
};
