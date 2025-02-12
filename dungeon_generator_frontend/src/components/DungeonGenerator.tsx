import { useState } from 'react';

const DungeonGenerator = () => {
  const [svgContent, setSvgContent] = useState('');
  const [descriptions, setDescriptions] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [selectedRoom, setSelectedRoom] = useState<string | null>(null);

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
  
  const handleRoomClick = (e: React.MouseEvent) => {
    const circle = (e.target as Element).closest('circle');
    if (circle) {
      const cx = circle.getAttribute('cx');
      const cy = circle.getAttribute('cy');
      if (cx && cy) {
        // 从圆形的中心坐标计算房间坐标
        const cell_size = 50; // 这需要与后端的 cell_size 匹配
        const x = Math.round((parseFloat(cx) / cell_size) - 0.5);
        const y = Math.round((parseFloat(cy) / cell_size) - 0.5);
        const key = `${x},${y}`;
        
        console.log("Clicked coordinates:", key); // 调试用
        
        if (descriptions[key]) {
          setSelectedRoom(key);
        } else {
          console.log("No description found for coordinates:", key); // 调试用
          setSelectedRoom(null);
        }
      }
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
          
          <div style={{ 
            display: 'flex',
            gap: '20px',
            marginTop: '20px'
          }}>
            {/* 地图区域 */}
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
                  onClick={handleRoomClick}
                  style={{ cursor: 'pointer' }}
                />
              ) : (
                <p style={{ color: '#666' }}>Click the button to generate a dungeon</p>
              )}
            </div>

            {/* 描述区域 */}
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
              {selectedRoom ? (
                <p>{descriptions[selectedRoom] || 'No description available for this room'}</p>
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