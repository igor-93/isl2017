import React from 'react';

import PageView from '../../layout/PageView';
import FollowingsList from "./FollowingsList";
import FollowingsDetails from "./FollowingsItemDetails";

import { connect } from 'react-redux';

import {FETCH_STATUS} from '../../../constants';

import {updateFollowingData, fetchUnfollowingUsers} from '../../../store/actions';

import 'Styles/targets.scss';
import Row from "../../layout/Row";
import Columns from "../../layout/Columns";

export default class FollowingsPage extends React.Component {

    constructor(props) {
        super();
        this.state = {
            selected_username: null,
        };
    }

    componentDidMount() {
        this.props.updateUnfollowingUsers();
    }

    handleClick(i) {
        this.setState({
            selected_username: this.props.users[i].username,
        });
    }

    _hideDetails() {
        this.setState({selected_username: null});
    }

    render() {
        const isExtended = Boolean(this.state.selected_username);
        const usersLoading = this.props.usersStatus.fetchStatus === FETCH_STATUS.FETCHING;
        const selectedUser = this.props.users.filter((user) => user.username === this.state.selected_username)[0];
        return (
            <PageView extended={isExtended} onHideDetails={() => this._hideDetails()}>
                <Row>
                    <Columns cols={[12, 6, 4]} className={'page-list-wrapper'}>
                        <FollowingsList loading={usersLoading} id="target-list" users={this.props.users} onClick={i => this.handleClick(i)} />
                    </Columns>

                    <Columns cols={[12, 12, 8]} className="page-details-wrapper">
                        <FollowingsDetails user={selectedUser} />
                    </Columns>
                </Row>
            </PageView>
        );
    }

}

FollowingsPage.propTypes = {
    fetchUnfollowUsers: React.PropTypes.func,
    updateUnfollowingUsers: React.PropTypes.func,
    users: React.PropTypes.arrayOf(React.PropTypes.object),
    usersStatus: React.PropTypes.object
};

FollowingsPage.defaultProps = {
    users: []
};

FollowingsPage.displayName = 'FollowingsPage';

/*CONTAINER COMPONENT*/
const mapStateToProps = (state, ownProps) => {
    return {
        users: state.unfollowingUsers,
        usersStatus: state.unfollowingUsersStatus
    }
};

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
        fetchUsers: () => dispatch(fetchUnfollowingUsers()),
        updateUnfollowingUsers: () => dispatch(updateFollowingData())
    };
};

export const SmartFollowingsPage = connect(
    mapStateToProps,
    mapDispatchToProps
)(FollowingsPage);

    
