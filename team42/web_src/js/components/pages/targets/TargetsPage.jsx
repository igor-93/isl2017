import React from 'react';

import PageView from '../../layout/PageView';
import TargetsList from "./TargetsList";
import TargetsItemDetails from "./TargetsItemDetails";

import {FETCH_STATUS} from '../../../constants';

import { connect } from 'react-redux';

import {untrackUser, updateTrackingData, fetchTrackedUsers, fetchTrackingData, fetchAggregatedTrackingData} from '../../../store/actions';

import 'Styles/targets.scss';
import ContentBox from "../../layout/ContentBox";
import {SmartUserSearch} from "./UserSearch";
import Row from "../../layout/Row";
import Columns from "../../layout/Columns";


export default class TargetsPage extends React.Component {

    constructor(props) {
        super();
        this.state = {
            selected_username: null
        };
    }

    componentDidMount() {
        this.props.updateTrackingData();
    }

    componentWillReceiveProps (nextProps) {

    }

    _handleClick(username) {
        const user = this._getUserFromUsername(username);
        if (!user._details_ts) {
            this._fetchDetails(user);
        }
        this.setState({selected_username: username});
    }

    _getUserFromUsername(username) {
        return this.props.users.filter((user) => user.username === username)[0];
    }

    _fetchDetails(user) {
        this.props.fetchUserDetails(user.username);
    }

    _hideDetails() {
        this.setState({selected_username: null});
    }

    _onRemoveUserClick(clickedUser) {
        this.props.untrackUser(clickedUser.username);
        this._hideDetails();
    }

    render() {
        const isExtended = Boolean(this.state.selected_username);
        const usersLoading = this.props.usersStatus.fetchStatus === FETCH_STATUS.FETCHING;
        return (
            <PageView extended={isExtended} onHideDetails={() => this._hideDetails()}>
                <Row>
                    <Columns cols={[12, 6, 4]} className={'page-list-wrapper'}>
                        <TargetsList loading={usersLoading} id="target-list" users={this.props.users} onClick={i => this._handleClick(i)} />
                    </Columns>

                    <Columns cols={[12, 12, 8]} className="page-details-wrapper">
                        <TargetsItemDetails user={this._getUserFromUsername(this.state.selected_username)} onRemoveUser={(user) => this._onRemoveUserClick(user)} />
                    </Columns>
                    <Columns cols={[12, 6]} className="page-other-wrapper">
                        <ContentBox title={'Add User'}>
                            <SmartUserSearch />
                        </ContentBox>
                    </Columns>
                </Row>
            </PageView>
        );
    }

}

TargetsPage.propTypes = {
    users: React.PropTypes.arrayOf(React.PropTypes.object),
    aggregatedData: React.PropTypes.object,
    usersStatus: React.PropTypes.object,
    fetchUsers: React.PropTypes.func,
    fetchUserDetails: React.PropTypes.func,
    fetchAggregatedData: React.PropTypes.func,
    updateTrackingData: React.PropTypes.func,
    untrackUser: React.PropTypes.func
};

TargetsPage.defaultProps = {
    users: [],
    aggregatedData: {},
    fetchUsers: () => {},
    fetchUserDetails: () => {},
    updateTrackingData: () => {},
    untrackUser: () => {}
};

TargetsPage.displayName = 'TargetsPage';

/*CONTAINER COMPONENT*/
const mapStateToProps = (state, ownProps) => {
  return {
      users: state.trackedUsers,
      usersStatus: state.trackedUsersStatus
  }
};

const mapDispatchToProps = (dispatch, ownProps) => {
  return {
      fetchUsers: () => dispatch(fetchTrackedUsers()),
      fetchUserDetails: (username) => dispatch(fetchTrackingData(username)),
      updateTrackingData: () => dispatch(updateTrackingData()),
      untrackUser: (username) => dispatch(untrackUser(username))
  };
};

export const SmartTargetsPage = connect(
  mapStateToProps,
  mapDispatchToProps
)(TargetsPage);

    
    
