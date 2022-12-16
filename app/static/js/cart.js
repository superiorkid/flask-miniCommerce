const addToCart = (productId) => {
  fetch(`${window.location.origin}/cart/${productId}/add`, {
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
  fetch(`${window.location.origin}/cart/${productId}/remove`, {
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

  temp = [];

  for (let i = 0; i < product.length; i++) {
    let cart = {
      name: product_name[i].innerHTML,
      price: price[i].innerHTML,
      quantity: quantity[i].value,
      cost: cost[i].innerHTML,
    };
    temp.push(cart);
  }

  let carts = { total: total.innerHTML, detail: temp };

  fetch(`${window.location.origin}/checkout`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(carts),
    headers: {
      "content-type": "application/json",
    },
  }).then((response) => {
    if (response.redirected) {
      window.location = response.url;
    }
  });
};
