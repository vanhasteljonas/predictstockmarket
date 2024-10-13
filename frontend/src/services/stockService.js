const API_BASE_URL = 'http://127.0.0.1:5000/api';

export const fetchStocks = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/stocks`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    throw new Error('There has been a problem with your fetch operation: ' + error.message);
  }
};

export const fetchStockData = async (stock, duration) => {
  try {
    const response = await fetch(`${API_BASE_URL}/stock_data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ stock, duration }),
    });
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    throw new Error('There has been a problem with your fetch operation: ' + error.message);
  }
};
