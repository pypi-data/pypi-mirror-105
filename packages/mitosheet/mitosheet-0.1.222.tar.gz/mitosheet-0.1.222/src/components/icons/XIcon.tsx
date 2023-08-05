// Copyright (c) Mito

import React from 'react';


const XIcon = (props: {width?: string, height?: string}): JSX.Element => {
    return (
        <svg width={props.width || "18"} height={props.height || "18"} viewBox="0 0 13 13" fill="none" xmlns="http://www.w3.org/2000/svg">
            <line x1="0.707107" y1="1.29289" x2="11.3136" y2="11.8994" stroke="#343434" strokeWidth="2"/>
            <line x1="0.7072" y1="11.8995" x2="11.3137" y2="1.29297" stroke="#343434" strokeWidth="2"/>
        </svg>
    )
}

export default XIcon;

