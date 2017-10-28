import React from 'react';

export default class Row extends React.Component {

    render() {
        return (
            <div className="row">
                {this.props.children}
            </div>
        );
    }

}

Row.propTypes = {
    children: React.PropTypes.node,
    className: React.PropTypes.string
};

Row.defaultProps = {
    className: ''
};

Row.displayName = 'Row';