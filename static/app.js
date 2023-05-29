async function getCupcakes() {
  const response = await axios.get('/api/cupcakes');
  for (let cupcake of response.data.cupcakes) {
    $('#cupcake-list').append(`
      <li>
        <img src="${cupcake.image}" alt="Cupcake Image">
        <br>
        ${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}
      </li>
    `);
  }
}

$('#new-cupcake-form').on('submit', async function(event) {
  event.preventDefault();
  const flavor = $('#flavor').val();
  const size = $('#size').val();
  const rating = $('#rating').val();
  const image = $('#image').val();

  const response = await axios.post('/api/cupcakes', {
    flavor, size, rating, image
  });

  $('#cupcake-list').append(`
    <li>
      ${response.data.cupcake.flavor} - ${response.data.cupcake.size} - ${response.data.cupcake.rating}
      <img src="${response.data.cupcake.image}" alt="Cupcake Image">
    </li>
  `);

  $('#new-cupcake-form').trigger('reset');
});

getCupcakes();
