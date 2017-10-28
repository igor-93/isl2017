/**
 * Created by Raphael on 14.03.2017.
 */
import React from 'react';
import ReactDom from 'react-dom';
import {initStore} from './store/storeUtils';
import Root from './components/Root';
import {initWebSockets} from './webSocketUtils';

import foundationStyles from '../styles/foundation.scss';
import appStyles from '../styles/app.scss';
import layoutStyles from 'Styles/layout.scss';
import postpageStyles from '../styles/post-pages.scss';

const store = initStore();

initWebSockets(store);

const rootElement = React.createElement(Root, {store: store}, null);

ReactDom.render(rootElement, document.getElementById('appRoot'), null);
