import React from 'react';
import FAIcon from "./FAIcon";

/**
 * Component to add texts which will be replaced by icons for small screens
 */
export default class IconText extends React.Component {

    render() {
        return (
            <span className="text-icon-alt">
                <span className="text-icon-alt-text">
                    {this.props.text}
                </span>
                <span className="text-icon-alt-icon">
                    <FAIcon title={this.props.text} iconName={this.props.iconName}/>
                </span>
            </span>
        );
    }

}

IconText.propTypes = {
    text: React.PropTypes.string,
    iconName: React.PropTypes.string
};

IconText.defaultProps = {
    iconName: '',
    text: ''
};

IconText.displayName = 'IconText';