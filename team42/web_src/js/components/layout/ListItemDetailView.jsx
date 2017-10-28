/**
 * Created by amirreza on 29.03.17.
 */

import React from 'react';

export default class ListItemDetailView extends React.Component {

    render() {
        return (
            <div className="list-item-detail-view">
                {this.props.children}
            </div>
        )
    }
}


ListItemDetailView.propTypes = {
    children: React.PropTypes.node
};

ListItemDetailView.defaultProps = {
};

ListItemDetailView.displayName = 'ListItemDetailView';
