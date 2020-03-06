import React, { useRef, useLayoutEffect } from 'react';
import gql from 'graphql-tag';
import { useParams } from 'react-router';
import { useSubscription } from '@apollo/react-hooks';

const FIGURE_SUBSCRIPTION = gql`
    subscription TestSubscription($instrumentAddress: String!) {
        waveform(instrumentAddress: $instrumentAddress) {
            figure
        }
    }
`;

export function Figure() {
    const { instrumentAddress } = useParams();
    const { data } = useSubscription(FIGURE_SUBSCRIPTION, {
        variables: {
            instrumentAddress: instrumentAddress.replace(/_/g, '.')
        }
    });
    const container = useRef();

    const figure = data ? data.waveform.figure : '';

    useLayoutEffect(() => {
        if (!(container.current && container.current.children[0])) {
            return;
        }
        
        container.current.children[0].setAttribute('height', '100%');
        container.current.children[0].setAttribute('width', '100%');
        container.current.children[0].setAttribute('preserveAspectRatio', 'none');
    });

    return (
        <div className='figure' dangerouslySetInnerHTML={{ __html: figure }} ref={container} />
    );
}
