

document.addEventListener('DOMContentLoaded', () => {
  
  const dropZone = document.getElementById('drop-zone');
  const fileInput = document.getElementById('file-input');
  const uploadDefault = document.getElementById('upload-state-default');
  const previewContainer = document.getElementById('preview-container');
  const imgPreview = document.getElementById('img-preview');
  const btnRemoveFile = document.getElementById('btn-remove-file');
  const captionInput = document.getElementById('caption-input');
  const btnAnalyze = document.getElementById('btn-analyze');
  const btnSpinner = document.getElementById('btn-spinner');
  const resultsBox = document.getElementById('results-box');

  const BACKEND_URL = "http://localhost:8000";
  let currentFile = null;
  let isUploading = false;

  
  function stripEmojis(text) {
    if (typeof text !== 'string') return text;
    
    return text.replace(/[\u{1F300}-\u{1F6FF}\u{1F900}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F000}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FAFF}\u{200d}\u{fe0f}\u{26A0}]/gu, '');
  }

  
  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!isUploading) dropZone.classList.add('dragover');
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('dragover');
    }, false);
  });

  dropZone.addEventListener('drop', (e) => {
    if (isUploading) return;
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  });

  
  dropZone.addEventListener('click', (e) => {
    if (isUploading) return;
    if (!currentFile && e.target !== btnRemoveFile) {
      fileInput.click();
    }
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      handleFileSelect(fileInput.files[0]);
    }
  });

  function handleFileSelect(file) {
    if (!file.type.match('image/jpeg') && !file.type.match('image/png') && !file.type.match('image/jpg')) {
      alert('Please upload a valid image file (PNG, JPG, or JPEG).');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('File size exceeds the 10MB limit.');
      return;
    }

    currentFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imgPreview.src = e.target.result;
      uploadDefault.style.display = 'none';
      previewContainer.style.display = 'block';
      btnAnalyze.removeAttribute('disabled');
      resultsBox.style.display = 'none';
    };
    reader.readAsDataURL(file);
  }

  
  btnRemoveFile.addEventListener('click', (e) => {
    e.stopPropagation();
    resetForm();
  });

  function resetForm() {
    currentFile = null;
    fileInput.value = '';
    captionInput.value = '';
    uploadDefault.style.display = 'flex';
    previewContainer.style.display = 'none';
    imgPreview.src = '';
    btnAnalyze.setAttribute('disabled', 'true');
    resultsBox.style.display = 'none';
  }

  
  btnAnalyze.addEventListener('click', () => {
    if (!currentFile || isUploading) return;

    isUploading = true;
    btnAnalyze.setAttribute('disabled', 'true');
    btnSpinner.style.display = 'inline-block';
    document.querySelector('.btn-text').textContent = 'Analyzing Screenshot...';
    resultsBox.style.display = 'none';

    const formData = new FormData();
    formData.append("file", currentFile);
    
    const captionVal = captionInput.value.trim();
    if (captionVal) {
      formData.append("caption", captionVal);
    }

    fetch(`${BACKEND_URL}/analyze`, {
      method: "POST",
      body: formData
    })
    .then(res => {
      if (!res.ok) {
        throw new Error(`Server returned status code: ${res.status}`);
      }
      return res.json();
    })
    .then(data => {
      console.log("Successfully connected to Peek AI backend.");
      renderResults(data);
    })
    .catch(err => {
      console.warn(`Backend connection error: ${err.message}. Falling back to offline simulator.`);
      setTimeout(() => {
        runSimulatedOfflineAnalysis();
      }, 1200);
    });
  });

  
  function renderResults(data) {
    resultsBox.innerHTML = '';

    
    const category = stripEmojis(data.category || "tech");
    const confidence = data.confidence || 100;
    const description = stripEmojis(data.description || "No description generated.");
    const ocr_text = stripEmojis(data.ocr_text || "");
    const detected_objects = (data.detected_objects || []).map(stripEmojis);
    const analysis = data.analysis || {};

    
    const titleEl = document.createElement('h3');
    titleEl.style.marginTop = '0';
    titleEl.style.borderBottom = '1px solid #333333';
    titleEl.style.paddingBottom = '8px';
    titleEl.style.fontSize = '18px';
    titleEl.textContent = "Analysis Results";
    resultsBox.appendChild(titleEl);

    
    const infoEl = document.createElement('p');
    infoEl.style.fontSize = '14px';
    infoEl.style.margin = '10px 0';
    infoEl.innerHTML = `<strong>Category Classified:</strong> ${category.toUpperCase()} (${confidence}% Match)`;
    resultsBox.appendChild(infoEl);

    
    const descEl = document.createElement('div');
    descEl.style.backgroundColor = '#f8f9fa';
    descEl.style.border = '1px solid #cccccc';
    descEl.style.padding = '12px';
    descEl.style.borderRadius = '4px';
    descEl.style.margin = '15px 0';
    descEl.style.fontSize = '14px';
    descEl.style.lineHeight = '1.6';
    descEl.innerHTML = `<strong style="display:block; margin-bottom:5px; color:#0056b3;">AI Analysis Description:</strong>${description}`;
    resultsBox.appendChild(descEl);

    
    const detailsEl = document.createElement('div');
    detailsEl.style.fontSize = '13px';
    detailsEl.style.lineHeight = '1.5';
    detailsEl.style.margin = '15px 0';
    
    const tagsString = detected_objects.length > 0 ? detected_objects.join(', ') : 'None';
    const ocrSnippet = ocr_text ? `"${ocr_text.substring(0, 120)}..."` : 'None detected.';
    
    detailsEl.innerHTML = `
      <strong style="color: #333333; font-size: 14px;">Detected Details:</strong>
      <div style="margin-top: 5px; padding-left: 10px; border-left: 2px solid #dddddd;">
        <div><strong>Raw OCR Text:</strong> ${ocrSnippet}</div>
        <div><strong>Extracted Keywords:</strong> ${tagsString}</div>
      </div>
    `;
    resultsBox.appendChild(detailsEl);

    
    const agentTitle = document.createElement('h4');
    agentTitle.style.margin = '20px 0 10px 0';
    agentTitle.style.fontSize = '15px';
    agentTitle.style.color = '#333333';
    agentTitle.textContent = `${category.charAt(0).toUpperCase() + category.slice(1)} Agent Analysis`;
    resultsBox.appendChild(agentTitle);

    const agentList = document.createElement('ul');
    agentList.style.fontSize = '13px';
    agentList.style.paddingLeft = '20px';
    agentList.style.lineHeight = '1.6';

    let listContent = '';
    if (category === 'food') {
      const mainDish = stripEmojis(analysis.recipe || 'N/A');
      const time = stripEmojis(analysis.cook_time || 'N/A');
      const cals = analysis.calories || 'N/A';
      const ingredients = (analysis.ingredients || []).map(stripEmojis).join(', ');
      const alternatives = (analysis.alternative_dishes || []).map(stripEmojis).join(', ');
      listContent = `
        <li><strong>Recipe Dish:</strong> ${mainDish}</li>
        <li><strong>Cook Time:</strong> ${time}</li>
        <li><strong>Calories:</strong> ${cals} kcal</li>
        <li><strong>Ingredients:</strong> ${ingredients}</li>
        <li><strong>Alternative Options:</strong> ${alternatives}</li>
      `;
    } else if (category === 'fashion') {
      const style = stripEmojis(analysis.estimated_style || 'N/A');
      const brand = stripEmojis(analysis.brand || 'N/A');
      const price = stripEmojis(analysis.price_range || 'N/A');
      const matches = (analysis.matching_outfits || []).map(stripEmojis).join(', ');
      listContent = `
        <li><strong>Style Category:</strong> ${style}</li>
        <li><strong>Brand:</strong> ${brand}</li>
        <li><strong>Price Range:</strong> ${price}</li>
        <li><strong>Suggested Outfits:</strong> ${matches}</li>
      `;
    } else if (category === 'books') {
      const author = stripEmojis(analysis.author || 'N/A');
      const genre = stripEmojis(analysis.genre || 'N/A');
      const summary = stripEmojis(analysis.summary || 'N/A');
      const similar = (analysis.similar_books || []).map(stripEmojis).join(', ');
      listContent = `
        <li><strong>Author:</strong> ${author}</li>
        <li><strong>Genre:</strong> ${genre}</li>
        <li><strong>Overview:</strong> ${summary}</li>
        <li><strong>Related Books:</strong> ${similar}</li>
      `;
    } else if (category === 'travel') {
      const dest = stripEmojis(analysis.destination || 'N/A');
      const budget = stripEmojis(analysis.budget || 'N/A');
      const hotels = (analysis.hotels || []).map(stripEmojis).join(', ');
      const activities = (analysis.things_to_do || []).map(stripEmojis).join(', ');
      listContent = `
        <li><strong>Destination:</strong> ${dest}</li>
        <li><strong>Budget Scale:</strong> ${budget}</li>
        <li><strong>Recommended Hotels:</strong> ${hotels}</li>
        <li><strong>Things to Do:</strong> ${activities}</li>
      `;
    } else if (category === 'movies') {
      const title = stripEmojis(analysis.movie_title || 'N/A');
      const actors = (analysis.actors || []).map(stripEmojis).join(', ');
      const plot = stripEmojis(analysis.plot || 'N/A');
      const platforms = (analysis.streaming_platforms || []).map(stripEmojis).join(', ');
      listContent = `
        <li><strong>Movie Title:</strong> ${title}</li>
        <li><strong>Actors:</strong> ${actors}</li>
        <li><strong>Plot Summary:</strong> ${plot}</li>
        <li><strong>Available Streaming:</strong> ${platforms}</li>
      `;
    } else { 
      const dev = stripEmojis(analysis.device || 'N/A');
      const price = stripEmojis(analysis.estimated_price || 'N/A');
      const specs = (analysis.specifications || []).map(stripEmojis).join(', ');
      const alternatives = (analysis.alternatives || []).map(stripEmojis).join(', ');
      listContent = `
        <li><strong>Device Model:</strong> ${dev}</li>
        <li><strong>Average Price:</strong> ${price}</li>
        <li><strong>Specifications:</strong> ${specs}</li>
        <li><strong>Alternatives:</strong> ${alternatives}</li>
      `;
    }

    agentList.innerHTML = listContent;
    resultsBox.appendChild(agentList);

    
    resultsBox.style.display = 'block';
    
    
    isUploading = false;
    btnAnalyze.removeAttribute('disabled');
    btnSpinner.style.display = 'none';
    document.querySelector('.btn-text').textContent = 'Analyze Screenshot';

    resultsBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  
  function runSimulatedOfflineAnalysis() {
    const captionVal = captionInput.value.toLowerCase();
    
    let category = "tech";
    let objects = ["Device", "Hardware"];
    let desc = "API is currently offline. Showing a simulated hardware classification.";
    let dynamicAnalysis = {
      device: "Standard Developer Laptop",
      estimated_price: "$1000",
      specifications: ["8GB RAM", "256GB SSD", "Full HD Display"],
      alternatives: ["Standard Desktop PC"]
    };

    if (captionVal.includes("ramen") || captionVal.includes("food") || captionVal.includes("eat")) {
      category = "food";
      objects = ["Noodles", "Bowl", "Soup"];
      desc = "API is currently offline. Showing a simulated food classification.";
      dynamicAnalysis = {
        recipe: "Quick Noodle Soup",
        cook_time: "10 mins",
        calories: 380,
        ingredients: ["Noodles", "Broth", "Seasonings"],
        alternative_dishes: ["Miso Noodle Soup"]
      };
    } else if (captionVal.includes("wear") || captionVal.includes("outfit") || captionVal.includes("fashion") || captionVal.includes("style")) {
      category = "fashion";
      objects = ["Shirt", "Outfit"];
      desc = "API is currently offline. Showing a simulated fashion classification.";
      dynamicAnalysis = {
        estimated_style: "Casual Everyday Wear",
        brand: "Generic Brand",
        price_range: "$20 - $50",
        matching_outfits: ["Jeans", "Sneakers"]
      };
    }

    const mockResponse = {
      category: category,
      confidence: 85,
      detected_objects: objects,
      ocr_text: "Local Offline Parsing",
      description: desc,
      analysis: dynamicAnalysis
    };

    renderResults(mockResponse);
  }
});
