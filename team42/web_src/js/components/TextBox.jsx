import React from 'react';

import 'Styles/text-box.scss';

export default class TextBox extends React.Component {

    render() {
        return (
            <div className={'text-box ' + this.props.className}>
                <div className="text-box-title">
                    <span>{this.props.title}</span>
                    <span>{this.props.info}</span>
                </div>
                <div className="text-box-text">
                    {this.props.children}
                </div>
            </div>
        );
    }

}

TextBox.propTypes = {
    title: React.PropTypes.string,
    children: React.PropTypes.node,
    className: React.PropTypes.string,
    info: React.PropTypes.string
};

TextBox.defaultProps = {
    title: '',
    className: '',
    info: '',
};

TextBox.displayName = 'TextBox';