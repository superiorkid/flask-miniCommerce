// initial value
let prices = document.getElementsByClassName("price");

function initialValue(price) {
  let temp = 0;
  for (let i = 0; i < prices.length; i++) {
    temp += parseFloat(price[i].innerHTML);
  }
  $("#total").html(temp);
}

initialValue(prices);
// initial value

/* Assign actions */
$(".product-quantity input").change(function () {
  updateQuantity(this);
});

/* Recalculate cart */
function recalculateCart() {
  var subtotal = 0;

  /* Sum up row totals */
  $(".product").each(function () {
    subtotal += parseFloat(
      $(this).children(".product-cost").children(".cost").text()
    );
  });

  /* Update totals display */
  $("#total").html(subtotal);
}

/* Update quantity */
function updateQuantity(quantityInput) {
  /* Calculate line price */
  var productRow = $(quantityInput).parent().parent();
  var price = parseFloat(
    productRow.children(".product-price").children(".price").text()
  );
  var quantity = $(quantityInput).val();
  var linePrice = price * quantity;

  /* Update line price display and recalc cart totals */
  productRow
    .children(".product-cost")
    .children(".cost")
    .each(function () {
      $(this).text(linePrice);
      recalculateCart();
    });
}
