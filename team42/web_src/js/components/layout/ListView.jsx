/**
 * Created by amirreza on 29.03.17.
 */

import React from 'react';
import LoadingSpinner from "../LoadingSpinner";
import SortFilterBar from "./SortFilterBar";

export default class ListView extends React.Component {

    _renderEmptyListMsg() {
        if (this.props.loading) {
            return null;
        }

        if (!this.props.children) {
            return <div className="list-view-empty-msg">{this.props.emptyListText}</div>;
        }

        if (Array.isArray(this.props.children) && this.props.children.length === 0) {
            return <div className="list-view-empty-msg">{this.props.emptyListText}</div>;
        }
        return null
    }


    render() {
        let moreButton = null;
        if (typeof this.props.onShowMoreClick === 'function') {
            moreButton = (
                <div className="show-more-box">
                    <button className="button show-more-button" onClick={(e) => this.props.onShowMoreClick(e)} disabled={this.props.loading}>Show More</button>
                </div>
            );
        }
        return (
            <div className="list-view">
                {this.props.loading && <LoadingSpinner absoluteCover/>}
                <div className="list-view-header">
                    <SortFilterBar sortFunc={this.props.sortFunc} filters={this.props.filters} onItemFuncChanged={this.props.onItemFuncChanged}/>
                </div>
                <div className="list-view-content">
                {this.props.children}
                {this._renderEmptyListMsg()}
                {moreButton}
                </div>
            </div>
        )
    }
}


ListView.propTypes = {
    children: React.PropTypes.node,
    onShowMoreClick: React.PropTypes.func,
    loading: React.PropTypes.bool,
    sortFunc: React.PropTypes.func,
    filters: React.PropTypes.arrayOf(React.PropTypes.shape({
        displayName: React.PropTypes.node,
        name: React.PropTypes.string.isRequired, // unique name as identifier
        filterFunc: React.PropTypes.func.isRequired
    })),
    onItemFuncChanged: React.PropTypes.func,
    emptyListText: React.PropTypes.string
};

ListView.defaultProps = {
    loading: false,
    onItemFuncChanged: () => {},
    filters: [],
    sortFunc: null,
    emptyListText: "No items available."
};

ListView.displayName = 'ListView';
