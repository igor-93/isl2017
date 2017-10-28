/**
 * Created by raphi on 18.03.2017.
 */
import React from 'react';
import {Provider} from 'react-redux';
import { URL } from '../constants';

import {SmartApp} from './App';

export default class Root extends React.Component {
    render() {
        return (
            <Provider store={this.props.store}>
                <SmartApp/>
            </Provider>
        );
    }
}

Root.propTypes = {
    store: React.PropTypes.object.isRequired
};

Root.defaultProps = {

};

Root.displayName = 'Root';
