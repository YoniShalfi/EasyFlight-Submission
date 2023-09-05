import React from 'react';
import refreshImage from './/refresh.jpg';

const RefreshButton = () => {
    const handleRefresh = () => {
        window.location.reload();
    };

    return (
        <div onClick={handleRefresh} style={{ cursor: 'pointer' }}>
            <img src={refreshImage} alt="Refresh" width="70" height="70" /> 
        </div>
    );
}

export default RefreshButton;
