import React from 'react';
import gql from 'graphql-tag';
import { useHistory, useParams } from 'react-router';
import { useMutation } from '@apollo/client';
import { Popconfirm, PageHeader, Button, Row, Col } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import { ChannelList } from '../../channels/components/channel-list';

const DELETE_INSTRUMENT = gql`
    mutation DeleteInstrument($address: String!) {
        deleteInstrument(address: $address) {
            id
        }
    }
`;

export function SingleInstrument() {
    const history = useHistory();
    const { instrumentAddress } = useParams();
    const [ deleteInstrument ] = useMutation(DELETE_INSTRUMENT, {
        variables: {
            address: instrumentAddress.replace(/_/g, '.')
        }
    });

    return (
        <>
            <PageHeader
                title={instrumentAddress}
                onBack={() => history.push('/')}
            />
            <ChannelList />
            <Row
                    justify='center'
                >
                <Col>
                    <Popconfirm
                        title={`Are you sure to remove ${instrumentAddress} with all its channels`}
                        okType='danger'
                        okText='Delete'
                        onConfirm={() => {
                            deleteInstrument();
                        }}
                    >
                        <Button
                            type='danger'
                            icon={<DeleteOutlined />}
                        >
                            {`Remove ${instrumentAddress}`}
                        </Button>
                    </Popconfirm>
                </Col>
            </Row>

        </>
    );
}
