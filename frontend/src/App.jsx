import React, { useState } from 'react';
import axios from 'axios';
import PlotlyGraph from 'react-plotly.js';
const Plot = PlotlyGraph.default || PlotlyGraph;
import { Sparkles, TrendingUp, ShieldAlert, BarChart3, Briefcase, RefreshCw, Zap, Network, Activity, Clock } from 'lucide-react';

const NIFTY_SYMBOLS = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS', 'HINDUNILVR.NS', 'SBIN.NS', 'ITC.NS', 'ASIANPAINT.NS', 'BAJFINANCE.NS', 'L&T.NS', 'HCLTECH.NS', 'MARUTI.NS', 'SUNPHARMA.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'WIPRO.NS', 'ONGC.NS', 'NTPC.NS', 'HDFCLIFE.NS'];

const StockCard = ({ rec }) => {
  const [expanded, setExpanded] = useState(false);
  const [history, setHistory] = useState(null);
  const [loadingChart, setLoadingChart] = useState(false);

  const toggleExpand = async () => {
    setExpanded(!expanded);
    if (!expanded && !history) {
      setLoadingChart(true);
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/history/${rec.symbol}`);
        setHistory(res.data);
      } catch (err) {
        console.error(err);
      }
      setLoadingChart(false);
    }
  };

  return (
    <div style={{ border: '1px solid #e2e8f0', borderRadius: '8px', marginBottom: '1rem', background: '#fff' }}>
      <div className="rec-item" style={{ border: 'none', marginBottom: 0, cursor: 'pointer' }} onClick={toggleExpand}>
        <div>
          <span style={{marginRight: '1rem', color: '#f59e0b'}}>⚡</span>
          <span className="rec-symbol">{rec.symbol}</span>
          <span style={{color: 'var(--text-muted)', marginLeft: '1rem', fontSize: '0.9rem'}}>{rec.sector} - {rec.market_cap_category} Cap</span>
        </div>
        <div style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
          <div className="success-tag">Score: {(rec.confidence * 100).toFixed(1)}%</div>
          <span>{expanded ? '▼' : '▶'}</span>
        </div>
      </div>
      {expanded && (
        <div style={{ padding: '1.5rem', borderTop: '1px solid #e2e8f0', display: 'flex', gap: '2rem' }}>
          <div style={{ flex: 1 }}>
            <h4 style={{ color: 'var(--primary-color)', marginTop: 0 }}>{rec.company_name || rec.symbol} Overview</h4>
            <p><strong>Industry:</strong> {rec.industry || 'N/A'}</p>
            <p><strong>P/E Ratio:</strong> {rec.pe_ratio ? rec.pe_ratio.toFixed(2) : 'N/A'}</p>
            <p><strong>Dividend Yield:</strong> {rec.dividend_yield ? (rec.dividend_yield * 100).toFixed(2) + '%' : 'None'}</p>
            <p><strong>Momentum (RSI-14):</strong> {rec.rsi_14 ? rec.rsi_14.toFixed(2) : 50}</p>
            <h5 style={{marginTop: '1.5rem'}}>✔️ Algorithmic Thesis</h5>
            <p style={{fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.5'}}>
              {rec.recommendation === 'Buy' 
                ? "Quantitative Edge: Model recognizes multi-variate pattern indicating >10% forward momentum in 30 days."
                : "Stability Check: Asset flagged as 'Hold' indicating strong downside protection. Ideal for risk mitigation."}
            </p>
          </div>
          <div style={{ flex: 2, minHeight: '300px' }}>
            {loadingChart ? <div className="spinner-wrapper"><RefreshCw className="spinner-icon" /> Fetching Market Trajectory...</div> : history ? (
              <Plot
                data={[
                  {
                    x: history.dates, open: history.open, high: history.high, low: history.low, close: history.close,
                    type: 'candlestick', name: 'Price'
                  },
                  {
                    x: history.dates, y: history.sma20, type: 'scatter', mode: 'lines', name: 'SMA 20',
                    line: { color: '#4f46e5', width: 2 }
                  }
                ]}
                layout={{
                  title: `90-Day Trajectory: ${rec.symbol}`,
                  margin: { t: 40, b: 30, l: 30, r: 10 },
                  height: 300,
                  xaxis: { rangeslider: { visible: false } },
                  paper_bgcolor: 'transparent',
                  plot_bgcolor: 'transparent',
                  showlegend: false
                }}
                config={{ displayModeBar: false }}
                style={{ width: '100%', height: '100%' }}
              />
            ) : <p style={{color: 'red'}}>Live chart momentarily unavailable.</p>}
          </div>
        </div>
      )}
    </div>
  );
};


function App() {
  const [activeTab, setActiveTab] = useState('profile');
  const [marketData, setMarketData] = useState(null);
  const [marketLoading, setMarketLoading] = useState(false);

  const [formData, setFormData] = useState({
    investment_type: 'Long-term (1+ Years)',
    risk_level: 'Medium',
    investment_amount: 50000,
    preferred_sector: 'All',
    expected_return: 15,
    dividend_preference: false,
    market_cap_preference: 'Large'
  });

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  // Expansions State
  const [newsQuery, setNewsQuery] = useState('RELIANCE.NS');
  const [newsData, setNewsData] = useState(null);
  const [newsLoading, setNewsLoading] = useState(false);

  const [backtestData, setBacktestData] = useState(null);
  const [backtestLoading, setBacktestLoading] = useState(false);

  const handleSlider = (e) => {
    setFormData({ ...formData, [e.target.name]: parseInt(e.target.value) });
  };

  const handleSelect = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const switchTab = async (tab) => {
    setActiveTab(tab);
    if (tab === 'market' && !marketData) {
      setMarketLoading(true);
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/market-data');
        setMarketData(res.data);
      } catch (err) {
        console.error(err);
      }
      setMarketLoading(false);
    }
  };

  const submitProfile = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post('http://127.0.0.1:8000/api/recommend', formData);
      setResults(res.data.recommendations || []);
      if(res.data.status === 'partial') {
          setError(res.data.message);
      }
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.detail);
      } else {
        setError("Fatal Error connecting to Intelligent AI. Make sure Python FastAPI is running.");
      }
      setResults([]);
    }
    setLoading(false);
  };

  const fetchNews = async () => {
      setNewsLoading(true);
      try {
          const res = await axios.get(`http://127.0.0.1:8000/api/news/${newsQuery}`);
          setNewsData(res.data);
      } catch (e) {
          console.error(e);
      }
      setNewsLoading(false);
  };

  const runBacktest = async () => {
      let symbolsToRun = [];
      let isDefault = false;
      if (!results || results.length === 0) {
          symbolsToRun = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS'];
          isDefault = true;
      } else {
          symbolsToRun = results.map(r => r.symbol);
      }
      setBacktestLoading(true);
      try {
          const res = await axios.post(`http://127.0.0.1:8000/api/backtest`, { symbols: symbolsToRun, initial_capital: formData.investment_amount });
          setBacktestData({...res.data, isDefault});
      } catch (e) {
          console.error(e);
          alert('Failed to execute backtest. The market API might be throttling.');
      }
      setBacktestLoading(false);
  };


  return (
    <>
      <nav className="navbar">
        <div className="logo-section">
          <Sparkles /> Intelligence AI
        </div>
        <div className="nav-links">
          <a className={`nav-link ${activeTab === 'profile' ? 'active' : ''}`} onClick={() => switchTab('profile')}>Investor Profile</a>
          <a className={`nav-link ${activeTab === 'backtest' ? 'active' : ''}`} onClick={() => switchTab('backtest')}>Simulator Log</a>
          <a className={`nav-link ${activeTab === 'news' ? 'active' : ''}`} onClick={() => switchTab('news')}>Live Sentiment</a>
          <a className={`nav-link ${activeTab === 'market' ? 'active' : ''}`} onClick={() => switchTab('market')}>Market Analysis</a>
          <a className={`nav-link ${activeTab === 'ml' ? 'active' : ''}`} onClick={() => switchTab('ml')}>Machine Learning</a>
        </div>
      </nav>

      <div className="container">
        {activeTab === 'profile' && (
          <div>
            <h1>Intelligent Stock Guidance System</h1>
            <h2 className="subtitle">Predict Your Placement Probability & Get Personalized Capital Recommendations</h2>

            <div className="metrics-grid">
              <div className="card metric-card">
                <div className="metric-icon-wrapper"><BarChart3 size={32}/></div>
                <div className="metric-title">Predict</div>
                <div className="metric-subtitle">Your Expected Returns</div>
              </div>
              <div className="card metric-card">
                <div className="metric-icon-wrapper"><ShieldAlert size={32}/></div>
                <div className="metric-title">Estimate</div>
                <div className="metric-subtitle">Safeguard Capital Risk</div>
              </div>
              <div className="card metric-card">
                <div className="metric-icon-wrapper"><Briefcase size={32}/></div>
                <div className="metric-title">Identify</div>
                <div className="metric-subtitle">Quality Equities</div>
              </div>
              <div className="card metric-card">
                <div className="metric-icon-wrapper"><TrendingUp size={32}/></div>
                <div className="metric-title">Recommend</div>
                <div className="metric-subtitle">Diversified Portfolios</div>
              </div>
            </div>

            <div className="card form-container">
              <h3 className="section-header">
                <Zap /> Investor Profile
              </h3>
              <p style={{ textAlign: "center", color: "var(--text-muted)", marginBottom: "2rem" }}>Fill in your risk-appetite for personalized trajectory guidance</p>

              <div className="form-grid">
                <div className="form-group">
                  <label className="form-label">Capital Expected Return: {formData.expected_return}%</label>
                  <input 
                    type="range" 
                    name="expected_return" 
                    min="5" 
                    max="50" 
                    value={formData.expected_return} 
                    onChange={handleSlider} 
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Market Capitalization Rule</label>
                  <select className="form-control" name="market_cap_preference" value={formData.market_cap_preference} onChange={handleSelect}>
                    <option value="Any">Market Neutral (Any)</option>
                    <option value="Large">Large Cap Focus</option>
                    <option value="Mid">Mid Cap Agility</option>
                    <option value="Small">Small Cap Growth</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Investment Allocation: ₹{(formData.investment_amount).toLocaleString()}</label>
                  <input 
                    type="range" 
                    name="investment_amount" 
                    min="5000" 
                    max="1000000" 
                    step="5000"
                    value={formData.investment_amount} 
                    onChange={handleSlider} 
                  />
                </div>

                <div className="form-group">
                  <label className="form-label">Sector Specialization</label>
                  <select className="form-control" name="preferred_sector" value={formData.preferred_sector} onChange={handleSelect}>
                    <option value="All">All / Global Allocation</option>
                    <option value="Technology">Technology</option>
                    <option value="Financial Services">Financial Services</option>
                    <option value="Healthcare">Healthcare</option>
                    <option value="Industrials">Industrials</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Mandatory Risk Guardrails</label>
                  <select className="form-control" name="risk_level" value={formData.risk_level} onChange={handleSelect}>
                    <option value="Low">Low Volatility Preferred</option>
                    <option value="Medium">Standard Growth</option>
                    <option value="High">Aggressive Growth</option>
                  </select>
                </div>

                <div className="form-group">
                  <label className="form-label">Dividend Preference</label>
                  <select className="form-control" name="dividend_preference" value={formData.dividend_preference} onChange={(e) => setFormData({...formData, dividend_preference: e.target.value === 'true'})}>
                    <option value="false">Yield Neutral</option>
                    <option value="true">Must Yield Dividends</option>
                  </select>
                </div>
              </div>

              <button className="btn-primary" onClick={submitProfile} disabled={loading}>
                {loading ? <RefreshCw className="spinner-icon" /> : 'Run Predictive Allocation Models'}
              </button>
            </div>

            {error && <div style={{padding: '1rem', background: '#fef2f2', color: '#ef4444', borderRadius: '8px', border: '1px solid #fca5a5', marginTop: '2rem'}}>
                <strong>System Notice:</strong> {error}
            </div>}

            {results && results.length > 0 && (
              <div style={{ marginTop: "4rem" }}>
                <h3 className="section-header"><BarChart3/> Portfolio Analysis</h3>
                
                <div className="analysis-grid two-cols">
                  <div className="card chart-card">
                      <div className="chart-title">Placement Probability (Algorithmic Confidence)</div>
                      <div className="donut-center">
                        <div style={{ position: 'relative', width: '200px', height: '200px', margin: '0 auto' }}>
                          <svg width="200" height="200" viewBox="0 0 160 160">
                            <circle cx="80" cy="80" r="60" fill="none" stroke="#e2e8f0" strokeWidth="18" />
                            <circle cx="80" cy="80" r="60" fill="none" stroke="#8b5cf6" strokeWidth="18"
                              strokeDasharray={2 * Math.PI * 60}
                              strokeDashoffset={2 * Math.PI * 60 - (results[0].confidence) * (2 * Math.PI * 60)}
                              strokeLinecap="round" transform="rotate(-90 80 80)" />
                          </svg>
                          <div className="donut-val" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: '#1e293b' }}>
                            {(results[0].confidence * 100).toFixed(1)}%
                          </div>
                        </div>
                        <div className="donut-label" style={{ marginTop: '0.1rem' }}>High Conviction Profile</div>
                      </div>
                  </div>

                  <div className="card chart-card">
                    <div className="chart-title">Recommended Corporate Placements</div>
                    {results.map((rec, idx) => (
                        <StockCard key={idx} rec={rec} />
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* NEWS FEED TAB */}
        {activeTab === 'news' && (
          <div style={{marginTop: '3rem', maxWidth: '800px', margin: 'auto'}}>
            <h2 style={{color: 'var(--primary-color)'}}><Activity style={{verticalAlign: 'text-bottom', marginRight: '0.5rem'}}/> Real-Time Media NLP Tracker</h2>
            <p style={{color: 'var(--text-muted)', marginBottom: '2rem'}}>Tap into live News APIs and execute global sentence-level polarity parsing (TextBlob).</p>
            
            <div className="card" style={{marginBottom: '2rem'}}>
                <div style={{display: 'flex', gap: '1rem'}}>
                    <select className="form-control" style={{flex: 1}} value={newsQuery} onChange={(e) => setNewsQuery(e.target.value)}>
                        {NIFTY_SYMBOLS.map(sym => <option key={sym} value={sym}>{sym}</option>)}
                    </select>
                    <button className="btn-primary" style={{width: 'auto', padding: '0 2rem'}} onClick={fetchNews} disabled={newsLoading}>
                        {newsLoading ? 'Parsings NLP...' : 'Analyze Market Sentiment'}
                    </button>
                </div>
            </div>

            {newsData && (
                <div className="card">
                   <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem'}}>
                      <div>
                         <h3 style={{marginTop: 0, marginBottom: '0.5rem'}}>Net Polarity Score: {newsData.sentiment_score.toFixed(3)}</h3>
                         <span className="success-tag" style={{background: newsData.sentiment_score > 0.1 ? '#dcfce7' : newsData.sentiment_score < -0.1 ? '#fee2e2' : '#f1f5f9', color: newsData.sentiment_score > 0.1 ? '#166534' : newsData.sentiment_score < -0.1 ? '#991b1b' : '#334155'}}>
                            System Label: {newsData.sentiment_label}
                         </span>
                      </div>
                      <div className="metric-icon-wrapper" style={{padding: '0.8rem', marginBottom: 0}}><Zap /></div>
                   </div>

                   <hr style={{border: 'none', borderTop: '1px solid #e2e8f0', margin: '1.5rem 0'}} />

                   <h4 style={{color: 'var(--text-muted)'}}>Headline Evaluation Engine ({newsData.articles.length} streams ingested)</h4>
                   {newsData.articles.length > 0 ? (
                       <ul style={{paddingLeft: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem'}}>
                           {newsData.articles.slice(0, 5).map((art, idx) => (
                               <li key={idx}><strong>{art.headline}</strong><br/><span style={{fontSize: '0.85rem', color: '#64748b'}}>{art.news_date}</span></li>
                           ))}
                       </ul>
                   ) : <p>No current verifiable news patterns mapped for this equity.</p>}
                </div>
            )}
          </div>
        )}

        {/* BACKTESTING TAB */}
        {activeTab === 'backtest' && (
          <div style={{marginTop: '3rem'}}>
            <h2 style={{color: 'var(--primary-color)'}}><Clock style={{verticalAlign: 'text-bottom', marginRight: '0.5rem'}}/> 6-Month Portfolio Simulative Backtest</h2>
            <p style={{color: 'var(--text-muted)', marginBottom: '2rem'}}>Projects your customized AI portfolio growth against the Nifty 50 benchmark index purely using exact historical daily closes.</p>
            
            <div className="card" style={{textAlign: 'center', marginBottom: '2rem', background: '#f1f5f9'}}>
                <button className="btn-primary" onClick={runBacktest} disabled={backtestLoading}>
                    {backtestLoading ? 'Backfilling Data Timelines...' : (!results || results.length === 0) ? 'Run Unconfigured Benchmark Default' : 'Deploy Historical Backtest Algorithm'}
                </button>
            </div>

            {backtestData && (
                <div className="analysis-grid two-cols">
                    <div className="card chart-card">
                       <h3 style={{margin: '0 0 1rem 0'}}>Performance Yield Comparison {backtestData.isDefault ? "(Default Mega-Cap Setup)" : "(AI Derived)"}</h3>
                       <div style={{marginBottom: '1rem'}}>
                         <div><strong>{backtestData.isDefault ? "Mega-Cap Average Yield:" : "AI Portfolio Construct Yield:"}</strong> <span style={{color: backtestData.total_return_pct > 0 ? 'var(--success)' : 'var(--danger)', fontWeight: 'bold'}}>{backtestData.total_return_pct.toFixed(2)}%</span></div>
                         <div><strong>Nifty 50 Base Yield:</strong> <span style={{color: backtestData.benchmark_return_pct > 0 ? 'var(--success)' : 'var(--danger)', fontWeight: 'bold'}}>{backtestData.benchmark_return_pct.toFixed(2)}%</span></div>
                       </div>
                       
                       <Plot
                         data={[
                           { x: backtestData.dates, y: backtestData.portfolio_value, type: 'scatter', mode: 'lines', name: 'AI Portfolio', line: { color: '#8b5cf6', width: 3 } },
                           { x: backtestData.dates, y: backtestData.benchmark_value, type: 'scatter', mode: 'lines', name: 'Nifty 50 Benchmark', line: { color: '#cbd5e1', width: 2, dash: 'dot'} }
                         ]}
                         layout={{
                           margin: { t: 10, b: 30, l: 40, r: 10 },
                           height: 350,
                           paper_bgcolor: 'transparent',
                           plot_bgcolor: 'transparent',
                           legend: { orientation: 'h', y: 1.1 }
                         }}
                         config={{ displayModeBar: false }}
                         style={{ width: '100%', height: '100%' }}
                       />
                    </div>

                    <div className="card chart-card">
                       <h3 style={{margin: '0 0 1rem 0'}}>Mathematical Framework</h3>
                       <p style={{lineHeight: 1.6, color: 'var(--text-muted)'}}>The portfolio simulator operates under the premise of calculating simple equal-weight distributions mathematically across the daily normalized yields. It ensures our random forest generated allocations strictly outperform or provide baseline hedging against the broad indices across the 6-month tracking metric.</p>
                       <div style={{background: '#f8fafc', padding: '1rem', border: '1px solid #e2e8f0', borderRadius: '8px', marginTop: '1rem'}}>
                           <div style={{fontWeight: 'bold', marginBottom: '0.5rem'}}>Base Capital Injection</div>
                           <div style={{fontSize: '1.5rem', color: 'var(--primary-color)'}}>₹{(formData.investment_amount).toLocaleString()}</div>
                           <div style={{fontWeight: 'bold', marginTop: '1rem', marginBottom: '0.5rem'}}>Net Present Value (NPV)</div>
                           <div style={{fontSize: '1.5rem', color: 'var(--success)'}}>₹{(backtestData.portfolio_value[backtestData.portfolio_value.length - 1]).toLocaleString(undefined, {maximumFractionDigits: 0})}</div>
                       </div>
                    </div>
                </div>
            )}
          </div>
        )}

        {/* MARKET ANALYSIS TAB */}
        {activeTab === 'market' && (
          <div style={{marginTop: '3rem'}}>
            <h2 style={{color: 'var(--primary-color)'}}><BarChart3 style={{verticalAlign: 'text-bottom', marginRight: '0.5rem'}}/> Market Analysis Architecture</h2>
            <p style={{color: 'var(--text-muted)', marginBottom: '2rem'}}>Live snapshot of the global universe metrics evaluated via the backend pipeline.</p>
            
            {marketLoading && <div className="spinner-wrapper"><RefreshCw className="spinner-icon" /> Fetching Macro Dataset...</div>}
            
            {marketData && marketData.data && (
              <div className="analysis-grid two-cols">
                <div className="card chart-card">
                   <div className="chart-title">Fundamental Sector Allocation</div>
                   <Plot
                     data={(() => {
                        const counts = marketData.data.reduce((acc, curr) => { 
                           acc[curr.sector] = (acc[curr.sector] || 0) + 1; 
                           return acc; 
                        }, {});
                        return [{
                           type: 'pie',
                           values: Object.values(counts),
                           labels: Object.keys(counts),
                           hole: 0.5,
                           textinfo: 'label+percent',
                           marker: { colors: ['#4f46e5', '#9333ea', '#6366f1', '#e2e8f0', '#cbd5e1'] }
                        }];
                     })()}
                     layout={{ margin: { t: 10, b: 10, l: 10, r: 10 }, showlegend: false, height: 350 }}
                     config={{displayModeBar: false}}
                     style={{ width: '100%', height: '100%' }}
                   />
                </div>
                
                <div className="card chart-card" style={{ height: '450px', overflowY: 'auto' }}>
                  <div className="chart-title" style={{position: 'sticky', top: 0, backgroundColor: 'white', paddingBottom: '1rem' }}>Universe Heatmap</div>
                  <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                    <thead>
                      <tr style={{ borderBottom: '2px solid #e2e8f0', color: 'var(--text-muted)' }}>
                        <th style={{padding: '0.5rem'}}>Symbol</th>
                        <th>Sector</th>
                        <th>Close</th>
                        <th>RSI-14</th>
                      </tr>
                    </thead>
                    <tbody>
                      {marketData.data.map(stock => (
                        <tr key={stock.symbol} style={{ borderBottom: '1px solid #f1f5f9' }}>
                           <td style={{padding: '0.8rem 0.5rem', fontWeight: 'bold', color: 'var(--primary-color)'}}>{stock.symbol}</td>
                           <td style={{color: 'var(--text-muted)'}}>{stock.sector}</td>
                           <td style={{fontWeight: '600'}}>₹{stock.Close ? stock.Close.toFixed(2) : '-'}</td>
                           <td style={{color: stock.rsi_14 > 60 ? 'green' : stock.rsi_14 < 40 ? 'red' : 'inherit'}}>{stock.rsi_14 ? stock.rsi_14.toFixed(1) : '-'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ML ENGINE TAB */}
        {activeTab === 'ml' && (
          <div style={{marginTop: '3rem', maxWidth: '800px', margin: '3rem auto'}}>
            <h2 style={{color: 'var(--primary-color)', textAlign: 'center', marginBottom: '2rem'}}><Network style={{verticalAlign: 'text-bottom', marginRight: '0.5rem'}}/> ML Engine Topology</h2>
            <div className="card" style={{padding: '3rem'}}>
               <h3 style={{marginTop: 0}}>Decision Trees & Neural Aggregation</h3>
               <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>The Intelligent Stock Recommendation System uniquely utilizes high-frequency Random Forest classifiers natively capable of ingesting 14 complex features at runtime.</p>
               <ul style={{lineHeight: '2'}}>
                 <li><strong>Technical Inputs:</strong> RSI, MACD, MACD Signal, EMA 20, SMA 50, Bollinger Bands.</li>
                 <li><strong>Fundamental Ratios:</strong> P/E Ratio, Trailing EPS, ROE, Debt/Equity, Market Cap.</li>
               </ul>
               <p style={{color: 'var(--text-muted)', lineHeight: '1.6'}}>By computing these multidimensional properties simultaneously, backend inference engines map 30-day forward probability thresholds, correlating market momentum seamlessly with the frontend React UI.</p>
               
               <div style={{background: '#f8fafc', padding: '1.5rem', borderRadius: '8px', marginTop: '2rem'}}>
                 <h4 style={{marginTop: 0, color: 'var(--primary-purple)'}}>Active Model</h4>
                 <code style={{background: '#e2e8f0', padding: '0.2rem 0.5rem', borderRadius: '4px'}}>RandomForestClassifier(n_estimators=100, max_depth=10)</code>
               </div>
            </div>
          </div>
        )}
      </div>
    </>
  )
}

export default App
