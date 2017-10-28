/**
 * Created by amirreza on 29.03.17.
 */

import React from 'react';

export default class ListItemView extends React.Component {

    render() {
        const clickable = typeof this.props.onClick === 'function';
        const clickFun = () => {
          if (clickable) {
              this.props.onClick();
          }
        };

        let className = 'list-item-view ';
        if (clickable) {
            className += 'clickable ';
        }
        if (this.props.selected) {
            className += 'selected ';
        }
        className += this.props.className;

        return (
            <div style={this.props.style} className={className} onClick={clickFun}>
                {this.props.children}
            </div>
        )
    }
}


ListItemView.propTypes = {
    children: React.PropTypes.node,
    onClick: React.PropTypes.func,
    className: React.PropTypes.oneOfType([React.PropTypes.string, React.PropTypes.number]),
    style: React.PropTypes.object,
    selected: React.PropTypes.bool
};

ListItemView.defaultProps = {
    onClick: null,
    className: '',
    style: {},
    selected: false
};

ListItemView.displayName = 'ListItemView';
