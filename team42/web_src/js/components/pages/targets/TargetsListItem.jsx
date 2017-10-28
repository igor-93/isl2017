import React from 'react';
import ListItemView from "../../layout/ListItemView";
import InstaUserLink from "../../layout/InstaUserLink";

export default class TargetsListItem extends React.Component {

    render() {
        const isAggregated = this.props.user.is_aggregated;
        let itemCss = '';
        if (isAggregated) {
            itemCss = 'target-item-aggregated';
        }

        return (
            <ListItemView className={itemCss} onClick={() => this.props.onClick(this.props.user.username)}>
                <div className={'list-item-content target-list-item '}>
                    <div className="item-img">
                        <img src={this.props.user.img_src_url || ''}/>
                    </div>
                    <div className="list-item-info">
                        <div><strong><InstaUserLink username={this.props.user.username}/></strong></div>
                        {!isAggregated && <div>{this.props.user.full_name}</div>}
                    </div>
                </div>
            </ListItemView>
        );
    }

}

TargetsListItem.propTypes = {
    onClick: React.PropTypes.func,
    user: React.PropTypes.object
};

TargetsListItem.defaultProps = {
    onClick: () => {},
    user: {}
};

TargetsListItem.displayName = 'TargetsListItem';