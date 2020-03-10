import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Switch, Route } from 'react-router';
import { Layout } from 'antd';
import { ApiProvider } from '../../api/components/api-provider';
import { SingleInstrument } from '../../instruments/components/single-instrument';
import { SingleChannel } from '../../channels/components/single-channel';
import { Figure } from '../../figure/components/figure';

export function App() {
    return (
        <ApiProvider>
            <Router>
                <Layout style={{height:"100vh"}}>
                    <Layout.Sider>
                        <Switch>
                            <Route path='/instruments/:instrumentAddress/channels/:channelName' component={SingleChannel} />
                            <Route path='/instruments/:instrumentAddress' component={SingleInstrument} />
                        </Switch>
                    </Layout.Sider>
                    <Layout.Content>
                        <Route path='/instruments/:instrumentAddress' component={Figure} />
                    </Layout.Content>
                </Layout>
            </Router>
        </ApiProvider>
    );
}
