$("#input-file").on("change", function () {
  // get the filename
  var path = $(this).val();
  var filename = path.replace(/^.*[\\\/]/, "");

  // replace the choose file label
  $(this).next(".custom-file-label").html(filename);
});
