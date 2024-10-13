import React, { useState, useEffect, useRef } from 'react';
import Select from 'react-select';
import { fetchStocks, fetchStockData } from '../services/stockService';
import StockChart from './../components/StockChart';


const Home = () => {
  const [stockOptions, setStockOptions] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [selectedDuration, setSelectedDuration] = useState('');
  const isInitialMount = useRef(true);  // Voeg useRef toe om de initiële mount te volgen
  const [showRsi, setShowRsi] = useState(true);
  const [stockData, setStockData] = useState(null);

  // Toggle-functie voor het tonen/verbergen van de RSI-lijn
  const toggleRsi = () => setShowRsi(!showRsi);

  const handleStockChange = (selectedOption) => {
    setSelectedStock(selectedOption);
  };

  const handleDurationChange = (event) => {
    setSelectedDuration(event.target.value);
  };

  // Fetch aandelen bij component mount
  useEffect(() => {
    const getStocks = async () => {
      const stocks = await fetchStocks();
      const options = stocks.map(stock => ({ value: stock, label: stock }));
      setStockOptions(options);
    };

    getStocks();
  }, []);

  // Update URL wanneer selectedStock of selectedDuration verandert
  useEffect(() => {
    if (isInitialMount.current) {
      isInitialMount.current = false;  // Schakel na de eerste render uit
    } else {
      // Update URL wanneer selectedStock of selectedDuration verandert
      const queryParams = new URLSearchParams();
      if (selectedStock) {
        queryParams.set('stock', selectedStock.value);
      }
      if (selectedDuration) {
        queryParams.set('duration', selectedDuration);
      }
      const newRelativePathQuery = window.location.pathname + '?' + queryParams.toString();
      window.history.replaceState(null, '', newRelativePathQuery);
    }
  }, [selectedStock, selectedDuration]);

  // Lees URL-parameters en stel de staat in bij component mount
  useEffect(() => { 
    const queryParams = new URLSearchParams(window.location.search);
    const stockQuery = queryParams.get('stock');
    const durationQuery = queryParams.get('duration');

    if (stockQuery) {
      setSelectedStock({ value: stockQuery, label: stockQuery });
    }
    if (durationQuery) {
      setSelectedDuration(durationQuery);
    }
  }, []);

  // Fetch stock data
  const handleSearch = async () => {
    if (selectedStock && selectedDuration) {
      const data = await fetchStockData(selectedStock, selectedDuration);
      setStockData(data);
      // renderChart(data);
    }
  };

  return (
    <div className="p-5">
      {/* Instellingen Sectie */}
      <div className="settings-section mb-4">
      <label htmlFor="stock-select" className="block text-sm font-medium text-gray-700">
          Choose a stock:
        </label>
        <Select
          id="stock-select"
          value={selectedStock}
          onChange={handleStockChange}
          options={stockOptions}
          className="basic-single"
          classNamePrefix="select"
          placeholder="Select a stock"
          isClearable
        />
        <label htmlFor="duration-select" className="block text-sm font-medium text-gray-700 mt-4">
          Select Duration
        </label>
        <select
          id="duration-select"
          value={selectedDuration}
          onChange={handleDurationChange}
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
        >
          <option value="">Choose a duration</option>
          <option value="1w">1 Week</option>
          <option value="1m">1 Month</option>
          <option value="6m">6 Months</option>
        </select>
      </div>

      <div className="mb-4">
        <button
          onClick={toggleRsi}
          className={`inline-flex items-center justify-center px-2 py-1 border border-transparent text-base rounded-md shadow-sm text-white ${
            showRsi ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'
          }`}
        >
          {showRsi ? 'Verberg RSI' : 'Toon RSI'}
        </button>
      </div>

      
      <div className="search-button-section mb-4 text-right">
        <button
          onClick={handleSearch}
          disabled={selectedDuration == null || selectedStock == null}
          className={`${(selectedDuration == null || selectedStock == null) ? "bg-blue-500 opacity-50" : "bg-blue-500 hover:bg-blue-700"} text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-2`}
          title={(selectedDuration == null || selectedStock == null) ? "Please select both a stock and a duration to enable search" : "Click to search"}
        >
          Search
        </button>
        {selectedDuration == "" || selectedStock == null ? (
          <p className="text-red-500 text-xs italic mt-2">
            Please select both a stock and a duration to enable the search.
          </p>
        ) : null}
      </div>

      {stockData ? (
        // Chart will be rendered here into another component using props from this component
        <StockChart data={stockData.data} showRsi={showRsi} />
      ) : (
        <div className="flex items-center justify-center bg-gray-200 rounded-lg p-4" style={{ minHeight: '200px' }}>
          No data visible yet
        </div>
      )}

    </div>
  );
};

export default Home;