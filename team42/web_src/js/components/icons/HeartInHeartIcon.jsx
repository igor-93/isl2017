import React from 'react';
import Icon from "./Icon";

export default class HeartInHeartIcon extends React.Component {

    render() {
        const innerSize = Math.min(1, Math.max(0, this.props.innerSize));
        const innerSizeString = 100 * innerSize + '%';
        return (
            <div className="heart-in-heart">
                <Icon name={Icon.ICONS.HEART} svgClass={'heart-in-heart-outer'} iconStyle={
                    {
                        fill: this.props.bgColor
                    }
                }/>
                <Icon name={Icon.ICONS.HEART} svgClass={'heart-in-heart-inner'} iconStyle={
                    {
                        width: innerSizeString,
                        height: innerSizeString,
                        fill: this.props.fillColor
                    }
                }/>
            </div>
        );
    }
}

HeartInHeartIcon.propTypes = {
    innerSize: React.PropTypes.number,
    fillColor: React.PropTypes.string,
    bgColor: React.PropTypes.string
};

HeartInHeartIcon.defaultProps = {
    innerSize: 0.5,
    fillColor: 'red',
    bgColor: 'none'
};

HeartInHeartIcon.displayName = 'HeartInHeartIcon';