import React from 'react';
import ListItemView from "../../layout/ListItemView";
import InstaUserLink from "../../layout/InstaUserLink";

export default class FollowingsListItem extends React.Component {

    _buildHslString(colorObj) {
        return 'hsl('+ colorObj.h  +',' + colorObj.s + '%,'+ colorObj.l + '%)';
    }

    _calcBgColor(activity) {
        let base = FollowingsListItem.COLOR_BASE_DEC;
        let lightness = 100;
        if (activity < 0) {
            return this._buildHslString({h: 0, s: 100, l: 100});
        }

        if (activity <= 1) {
            lightness = base.l + (100 - base.l) * activity;
        } else {
            base = FollowingsListItem.COLOR_BASE_ASC;
            lightness = 100 - ((100 - base.l) * (Math.min(activity - 1, 1)));
        }

        return this._buildHslString({h: base.h, s: base.s, l: lightness});
    }

    render() {
        const activityColor = this._calcBgColor(this.props.user.activity);

        return (
            <ListItemView className={'force-clickable'} style={{backgroundColor: activityColor}} onClick={() => this.props.onClick()}>
                <div className={'list-item-content following-list-item'}>
                    <div className="item-img">
                        <img src={this.props.user.img_src_url || ''}/>
                    </div>
                    <div className="list-item-info">
                        <div><strong><InstaUserLink username={this.props.user.username}/></strong></div>
                        <div>{this.props.user.full_name}</div>
                    </div>
                </div>
            </ListItemView>
        );
    }

}

FollowingsListItem.propTypes = {
    onClick: React.PropTypes.func,
    user: React.PropTypes.object
};

FollowingsListItem.defaultProps = {
    onClick: () => {},
    user: {}
};

FollowingsListItem.displayName = 'FollowingsListItem';

FollowingsListItem.COLOR_BASE_DEC = {
    h: 0,
    s: 100,
    l: 80
};

FollowingsListItem.COLOR_BASE_ASC = {
    h: 120,
    s: 100,
    l: 80
};