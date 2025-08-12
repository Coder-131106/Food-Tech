async function recognizeFood() {
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  if (!file) return alert('Please upload an image');

  const formData = new FormData();
  formData.append('file', file);

  const previewContainer = document.getElementById('previewContainer');
  const resultDiv = document.getElementById('result');
  previewContainer.innerHTML = '';
  resultDiv.innerHTML = '';

  const img = document.createElement('img');
  img.src = URL.createObjectURL(file);
  img.className = 'preview';
  previewContainer.appendChild(img);

  const res = await fetch('http://localhost:5000/predict', {
    method: 'POST',
    body: formData
  });
  const data = await res.json();

  resultDiv.innerHTML = `
    <h3>Food: ${data.name}</h3>
    <p>${data.summary}</p>
    <ul>${data.ingredients.map(i => `<li>${i}</li>`).join('')}</ul>
  `;
}
