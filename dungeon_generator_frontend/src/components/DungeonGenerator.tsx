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
      console.log('开始请求API...');
      const response = await fetch('https://four60-rulebasesystem.onrender.com/api/generate-dungeon');
      console.log('收到响应:', response);
      
      const data = await response.json();
      console.log('解析后的数据:', data);
      
      console.log('Setting SVG content...');
      setSvgContent(data.svg);
      console.log('SVG content set!');
      
      console.log('Setting descriptions...');
      setDescriptions(data.descriptions);
      console.log('Descriptions set!');
    } catch (error) {
      console.error('详细错误信息:', error);
    } finally {
      setLoading(false);
    }
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
                        const x = Math.round((parseFloat(cx) / 50) - 0.5);
                        const y = Math.round((parseFloat(cy) / 50) - 0.5);
                        const key = `${x},${y}`;
                        setSelectedRoom(key);
                      }
                    }
                  }}
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