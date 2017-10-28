/**
 * Created by amirreza on 29.03.17.
 */

import React from 'react';
import FAIcon from "../icons/FAIcon";
export default class PageView extends React.Component {

    _onCloseButtonClick() {
        this.props.onHideDetails();
    }

    render() {
        return (
                <div className={'page-view ' + this.props.className + (this.props.extended ? ' show-details' : '')}>
                    <div className="page-view-header">
                        <div className={(this.props.title ? 'page-view-title' : '')}>
                            {this.props.title}
                        </div>
                        <button className="no-margin secondary button small details-close-button" onClick={() => this._onCloseButtonClick()}>
                            <FAIcon iconName={'close'}/>
                        </button>
                    </div>
                    <div className="page-view-content">
                        {this.props.children}
                    </div>
                </div>
        );
    }
}




PageView.propTypes = {
    children: React.PropTypes.node,
    title: React.PropTypes.string,
    className: React.PropTypes.string,
    extended: React.PropTypes.bool,
    onHideDetails: React.PropTypes.func
};

PageView.defaultProps = {
    className: '',
    title: '',
    onHideDetails: () => {}
};

PageView.displayName = 'PageView';
