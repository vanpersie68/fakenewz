<template>
  <section>
    <div class="invite">

     <p class="title">{{ survey_name }}</p>

      <div class="ui">
        <!-- Invite box -->
        <p class="account">{{ $t('g5.Invite Users') }}</p>
        <img alt="" class="line" src="imagesine.png" />
        <p class="inputbox">{{ $t('g5.Enter Email') }}</p>
        <div>
          <input class="email-input" type="text" v-model="inviteEmail" placeholder="Enter email" />
        </div>
        <div class="error">
          <div id="invite-error-message"></div>
        </div>
        <img alt="" class="line" src="imagesine.png" />
        <div>
          <button @click="sendInvite" class="invite-button">
            {{ $t('g5.Invite') }}
          </button>
        </div>
      </div>
    </div>

    <div class="space"></div>

    <div class="collaborators">
          <p class="account">{{ }}</p>
          <form name="collaborators">
            <div class="table-container">
                <table>
                  <thead>
                    <tr>
                      <th colspan="3">{{ $t('g5.Existing Collaborators') }}</th>
                    </tr>
                    <tr>
                      <th>{{ $t('g5.Username') }}</th>
                      <th>{{ $t('g5.Email') }}</th>
                      <th>{{ $t('g5.Actions') }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(collab, index) in collaborator" :key="index">
                      <td>{{ collab.username }}</td>
                      <td>{{ collab.email }}</td>
                      <td>
                        <button @click="removeCollaborator(collab.id)">{{ $t('g5.Remove') }}</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
            </div>
          </form>
      </div>

    <div class="space"></div>
  </section>
</template>

<script>
import pubsub from 'pubsub-js'
import axios from 'axios';
import SurveyServices from '../services/SurveyServices'

export default {
  name: 'InviteUsers',
  data() {
    return {
      survey_id: this.$route.params.id,
      survey_name: this.$route.params.name,
      inviteEmail: '',
      collaborator: [], // Existing collaborators from the backend
    }
  },
  methods: {
    async fetchCollaborators() {
      SurveyServices.getCollaborators(this.survey_id)
      .then((collaborator) => {
        this.collaborator = collaborator;
      })
      .catch((error) => {
        console.error('Error fetching collaborators:', error);
      });
    },
    goToMainPage() {
      //redirect to the user profile page
      this.$router.push(`/My_Survey`)
    },
    sendInvite() {
        const websiteUrl = `http://111.231.14.233:8080/`;
        //const websiteUrl = `https://fakenewz.info/`;
        const url = `http://111.231.14.233:8080/accept-invitation?token=${localStorage.getItem('token')}&id=${this.survey_id}`;

        this.$axios
            .post('account/send-invite/', { email: this.inviteEmail,
                                        websiteUrl: websiteUrl,
                                        username: localStorage.getItem('username'),
                                        surveyid: this.survey_id,
                                        surveyname: this.survey_name})
            .then((response) => {
                // Invitation sent successfully, show a confirmation message
                alert(response.data.message)
            })
            .catch((error) => {
            // Handle error
            alert('Failed, please check if your email is valid.', error)
            window.location.reload()
            });
    },
    removeCollaborator(user_id){
        this.$axios
            .post('survey/collaborators/delete/', {survey_id: this.survey_id,
                                                   user_id: user_id})
            .then(() => {
                alert('Delete successfully.');
                window.location.reload()
            })
            .catch((error) => {
            // Handle error
            alert('Failed, please try again.'+error)
            window.location.reload()
            });
    }
  },
  created() {
    // Call the method to fetch collaborators when the component is created
    this.fetchCollaborators();
  },
}
</script>

<style scoped>

.title {
  font-size: 36px; /* Adjust the font size as needed */
  font-weight: bold;
  text-align: center; /* Center the text horizontally */
  margin-top: 50px; /* Adjust the top margin to center vertically */
}

.invite {
  position: relative;
}

.space {
  height: 40px;
}


.collaborator {
  display: flex;
  justify-content: space-between;
  flex-basis: 45%;
  margin: 0 auto;
}

.table-container {
  margin: 0 auto;
  width: 80%;
}

table {
  border-collapse: collapse;
  width: 100%;
}

table, th, td {
  border: 1px solid #000;
}

th, td {
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.ui {
  background-color: white;
  border-radius: 16px;
  padding: 20px 0 18px;
  border: 2px solid black;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  justify-content: flex-end;
  width: 450px;
  margin: 0 auto;
  margin-top: 30PX;
  flex-basis: 45%;
}

.account {
  font-size: 24px;
  font-weight: 700;
  line-height: normal;
  color: black;
  margin: 0 auto;
  text-align: center;
}
.line {
  width: 100%;
  margin-bottom: 15px;
}
.inputbox {
  width: 400px;
  font-size: 16px;
  font-weight: 700;
  line-height: normal;
  color: dimgray;
  margin-bottom: 9px;
}
.email-input {
  width: 396px;
  height: 32px;
  background-color: white;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 2px solid linen;
}
.error {
  background: #ffc199; /*Change background color*/
  border-left: 9px solid #ff6600; /*Change left border color*/
  color: #2c3e50; /*Change text color*/
  width: 90%;
  font-size: 16px;
  font-weight: 700;
  line-height: normal;
  margin-bottom: 4px;
}

.back-button {
  background: none;
  border: 1px solid black;
  margin-bottom: 18px;
  border-radius: 8px;
  padding: 13px 20px;
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
}
.back-button:hover {
  opacity: 0.3;
  cursor: pointer;
}

.invite-button {
  background: none;
  border: 1px solid black;
  margin-bottom: 18px;
  border-radius: 8px;
  padding: 13px 20px;
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
}
.invite-button:hover {
  opacity: 0.3;
  cursor: pointer;
}
</style>