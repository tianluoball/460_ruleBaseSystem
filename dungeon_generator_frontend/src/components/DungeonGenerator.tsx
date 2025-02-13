import { useState } from 'react';

const DungeonGenerator = () => {
  const [svgContent, setSvgContent] = useState('');
  const [descriptions, setDescriptions] = useState<Record<string, string>>({});
  const [overview, setOverview] = useState('');
  const [theme, setTheme] = useState('');
  const [selectedRoom, setSelectedRoom] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const generateDungeon = async () => {
    setLoading(true);
    setDescriptions({});
    setSelectedRoom(null);
    
    try {
      const response = await fetch('https://four60-rulebasesystem.onrender.com/api/generate-dungeon');
      const data = await response.json();
      console.log('Received descriptions:', data.descriptions);  // 调试用
      setSvgContent(data.svg);
      setDescriptions(data.descriptions);
      setOverview(data.overview);
      setTheme(data.theme);
    } catch (error) {
      console.error('Error generating dungeon:', error);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ 
        border: '1px solid #ccc', 
        borderRadius: '8px', 
        padding: '20px',
        backgroundColor: 'white'
      }}>
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ marginBottom: '20px' }}>Dungeon Generator</h2>
          <button 
            onClick={generateDungeon}
            disabled={loading}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: loading ? '#ccc' : '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Generating...' : 'Generate Dungeon'}
          </button>
          
          {overview && (
            <div style={{ 
              marginTop: '20px',
              padding: '15px',
              backgroundColor: '#f8f9fa',
              borderRadius: '4px',
              textAlign: 'left',
              whiteSpace: 'pre-line'
            }}>
              {overview}
            </div>
          )}

            {/* example */}
          <div style={{
            padding: '15px',
            backgroundColor: '#f8f9fa',
            borderRadius: '4px',
            marginBottom: '20px'
          }}>
            <h3 style={{ marginBottom: '10px' }}>Room Types:</h3>
            <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#4CAF50' }}></div>
                <span>S - Entrance</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#7B1FA2' }}></div>
                <span>M - Monster Room</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#FFD700' }}></div>
                <span>T - Treasure Room</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <div style={{ width: '20px', height: '20px', borderRadius: '50%', backgroundColor: '#F44336' }}></div>
                <span>X - Exit</span>
              </div>
            </div>
          </div>
          
          <div style={{ 
            display: 'flex',
            gap: '20px',
            marginTop: '20px'
          }}>
            {/* Map Area */}
            <div style={{ 
              flex: '1',
              backgroundColor: '#f8f9fa',
              borderRadius: '4px',
              padding: '20px',
              minHeight: '400px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              {svgContent ? (
                <div 
                  dangerouslySetInnerHTML={{ __html: svgContent }}
                  onClick={(e) => {
                    const circle = (e.target as Element).closest('circle');
                    if (circle) {
                      const cx = circle.getAttribute('cx');
                      const cy = circle.getAttribute('cy');
                      if (cx && cy) {
                        // 修改坐标计算方式
                        const cell_size = 50;
                        const x = Math.floor(parseFloat(cx) / cell_size - 0.5);
                        const y = Math.floor(parseFloat(cy) / cell_size - 0.5);
                        const key = `${x},${y}`;
                        console.log('Clicked coordinates:', key);  // 调试用
                        console.log('Available descriptions:', Object.keys(descriptions));  // 调试用
                        setSelectedRoom(key);
                      }
                    }
                  }
                }
                  style={{ cursor: 'pointer' }}
                />
              ) : (
                <p style={{ color: '#666' }}>Click the Generate button to create a dungeon</p>
              )}
            </div>

            {/* Description Area */}
            <div style={{
              flex: '1',
              backgroundColor: '#f8f9fa',
              borderRadius: '4px',
              padding: '20px',
              minHeight: '400px',
              display: 'flex',
              flexDirection: 'column',
              gap: '10px'
            }}>
              <h3>Room Description</h3>
              {theme && <p style={{ color: '#666' }}>Theme: {theme}</p>}
              {selectedRoom ? (
                <p style={{ fontSize: '16px', lineHeight: '1.6' }}>
                  {descriptions[selectedRoom] || 'Select a room to view its description'}
                </p>
              ) : (
                <p style={{ color: '#666' }}>Click on a room to view its description</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DungeonGenerator;