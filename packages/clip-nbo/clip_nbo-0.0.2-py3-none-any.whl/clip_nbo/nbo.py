from .helpers.utils import Utils
from .models.rnn import RNN
from .predict.predict import NBO
from .helpers.transformation import Transform
import tensorflow as tf
import warnings
import pandas as pd
import os
from tensorflow import keras
import numpy as np

class NextBestOffering(object):
    """
    This package is about training and prediction the next best categories,
    it includes 2 methods train() and predict()
    """
    pd.set_option('mode.chained_assignment', None)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

    @classmethod
    def train(cls, source_full_file_name, client_name, number_of_visits, category_number):
        """
        Method to train GRU and LSTM models for Next Best Offering
        Args:

            source_full_file_name(dataframe): url for source file to be trained using GRU and LSTM
            client_name(str): client home directory name
            number_of_visits(int): number of visits entered to the training -1
            category_number(int): number of categories in each visit

        Returns:
            modelUrl(str): model file full path
            featuresList(list): columns that final model training on them
            rnnType(str): string represent the rnn type that the training created with (LSTM, GRU)
            predictionScore(float): final model accuracy on the testing dataset

        """
        tf.compat.v1.disable_eager_execution()
        # warnings.filterwarnings("ignore", category=DeprecationWarning)

        try:

            # read the data file
            source_data = Utils().read_data(source_full_file_name)
            # print('Input data source ')
            # print(source_data)
            # print(source_data.info())

            # input data selection without swapping
            # data_scoping = Utils().data_scoping(source_data, 'train')
            # print(' all dataset before omar function', source_data.count())
            # source_data = source_data[['Visit_3_Cat_1', 'Visit_2_Cat_1', 'Visit_1_Cat_1']]
            # data_scoping = source_data.dropna(subset=['Visit_3_Cat_1', 'Visit_2_Cat_1', 'Visit_1_Cat_1'])
            # data_scoping = Utils().data_preparation(source_data, 5, 3)


            # parameters to mahmoud akeel for swapping
            # number_of_visits = 3
            # category_number = 5
            start_from_visit = 1

            # data selection for swapping idea
            df, main_visits = Transform().visits_categories_columns(source_data, number_of_visits, category_number,
                                                                    start_from_visit)
            # print('----------------------------------------------')
            # print('---- we are after visits_categories_columns---')
            # print('----------------------------------------------')
            # print('main_visits  :  ', main_visits)
            # print('df : ', df.head(2))
            train_x, train_y = Transform().swapping(df, category_number, number_of_visits, main_visits)

            train_x, train_y, x_features = Transform().one_hot_encoding_training_data(train_x, train_y)

            labels = train_y.columns

            # print(' all dataset after omar function', train_x.count())
            # print(train_x.head(2))
            # print('train_x : ', train_x.shape)
            # print('train_y : ', train_y.shape)
            # print('x_features : ', x_features.shape)
            #
            # print('------------------------checkssssssssssssss-------------------')

            # train_x, train_y, val_x, val_y, test_x, test_y = Transform().nbo_split_data_test(train_x, train_y, 0.10)
            # x_trn_reshaped, x_trn, y_trn, x_val_reshaped, x_val, y_val, x_tst_reshaped, x_tst, y_tst\
            x_trn_reshaped, x_trn, y_trn, x_val_reshaped, x_val, y_val, x_tst_reshaped, x_tst, y_tst \
                = Transform().nbo_split_data_test(train_x, train_y, 0.10)
            #print('shape of x : ', train_x.shape)
            # print('shape of y : ', train_y.shape)

            # print('train_x:', train_x)
            # print('train_y: ', train_y)

            # Training the model with auto trainer and auto evaluator
            final_results = RNN().model_trainer(x_trn_reshaped, y_trn, x_val_reshaped, y_val, x_tst_reshaped, y_tst)
            # final_results = RNN().model_trainer(x_trn, y_trn, x_val, y_val, x_tst, y_tst)
            # final_results = RNN().model_trainer(x_trn_reshaped, y_trn, x_val_reshaped, y_val, x_tst_reshaped, y_tst,
            #                                     classes)

            # final_results = RNN().model_trainer(train_x, train_y, val_x, val_y, test_x, test_y)
            # print('-------------final results-------------')
            # print(final_results)

            # save the model object with check option

            #final_results[2].save_weights("ckpt")
            #load_status = final_results[2].load_weights("ckpt")

            model_file_path = Utils().save_pipeline(final_results[2], Utils().generate_file_name('model'), client_name)
            # scaler_file_path = Utils().save_pickle(scaler, Utils().generate_file_name('scalar'), client_name)

            # Delete the weights files after all experiments
            Utils().clean_best_model_file(client_name)

            # return Utils.with_success({
            #     "scalerUrl": scaler_file_path,
            #     "modelUrl": model_file_path,
            #     "featuresList": training_columns,
            #     "predictionScore": round(final_results[1], 2)  # this should be reported on the testing sets
            # })
            return Utils.with_success({
                "modelUrl": model_file_path,
                "featuresList": x_features.tolist(),
                "rnnType": final_results[3],
                "predictionScore": round(final_results[1], 2),# this should be reported on the testing sets
                "labels":labels
            })
        except Exception as err:
            return Utils().with_error(0, '', err)

    @classmethod
    def predict(cls,source_full_file_name, model_file_name, features_name, number_of_predict_visits,category_number, client_name, labels):
        # def predict(cls, source_full_file_name, model_file_name, scaler_file_name, training_columns, client_name):

        """
        Method to predict CNN model for churn prediction data
        Args:
            source_full_file_name(str): source data frame file full path
            model_file_name(str): model file full path
            features_name(list): final model accuracy on the testing dataset
            number_of_predict_visits(int): number of visits entered to the training -1
            category_number(int): number of categories in each visit
            client_name(str): client home directory name
        Returns:
            predictionFileUrl(str): output file full path
        """

        try:
            predict = NBO()

            # read the data file
            source_data = Utils().read_data(source_full_file_name)
            # print(source_data.head(2))
            # Dummies = Transform().one_hot_encoding_data(source_data, features_name, number_of_vistis)
            # print(df_predict.head())
            # print(IDS.head())
            start_from_visit = 1
            df_predict, IDS = Transform().visits_categories_columns_prediction(source_data, number_of_predict_visits,
                                                                               category_number, start_from_visit)
            # print(df_predict.head())
            # print(IDS.head())

            df_predict = Transform().predict_non_zero(df_predict, category_number, number_of_predict_visits)
            df_predict_dummies = Transform().one_hot_encoding_predictions(df_predict, number_of_predict_visits,
                                                                          features_name)

            df = df_predict_dummies
            
            # load the model object
            try:
                model = tf.keras.models.load_model('test_model.h5',custom_objects= {'f1_micro': RNN().f1_micro,'f1_macro':RNN().f1_macro})
            except Exception as err:
                Utils().with_error(2, 'The h5 file does not exist !!', err)


            # predict the model
            df_predict=df.values
            df_predict = df_predict.reshape(-1, df_predict.shape[1], 1)
            df_predict = df_predict.astype('float32') 
            classes_prob = model.predict(df_predict)
            sorted_classes = np.argsort(classes_prob)
            sorted_classes = sorted_classes[:,-5:]
            
            first_classes = sorted_classes[:,-1]
            
            print(labels)
            print(labels)
            print(labels)
            print(labels)

            df['first_predicton'] =  [labels[i] for i in sorted_classes[:,-1]]
            df['second_predicton'] = [labels[i] for i in sorted_classes[:,-2]]
            df['third_predicton'] =  [labels[i] for i in sorted_classes[:,-3]]
            df['fourth_predicton'] = [labels[i] for i in sorted_classes[:,-4]]
            df['fifth_predicton'] =  [labels[i] for i in sorted_classes[:,-5]]

            df['CustomerId'] = IDS
            
            if not ('CustomerId' in df.columns):
                return Utils().with_error(6, 'The ID column does not exist')
            
            df = df[['CustomerId','first_predicton','second_predicton','third_predicton','fourth_predicton','fifth_predicton']]

            
            # save the prediction result in the file
            output_full_file_name = Utils().write_csv_file(df, client_name)
            
            # return the output
            return Utils().with_success({
                "predictionFileUrl": output_full_file_name
            })

        except Exception as err:
            return Utils().with_error(0, '', err)


    # comments from initial trials of nbo and churn prediction
    # -----------------------------------------------------------
    # @classmethod
    # def train(cls, source_full_file_name, client_name):
    #     """
    #     Method to train CNN model for churn prediction
    #     Args:
    #         source_full_file_name(dataframe): url for source file to be trained using GRU and LSTM
    #         client_name(str): client home directory name
    #     Returns:
    #         scalerUrl(str): scaler file full path
    #         modelUrl(str): model file full path
    #         featuresList(list): columns that final model training on them
    #         predictionScore(float): final model accuracy on the testing dataset
    #
    #     """
    #     tf.compat.v1.disable_eager_execution()
    #     # warnings.filterwarnings("ignore", category=DeprecationWarning)
    #
    #     # try:
    #
    #     # read the data file
    #     source_data = Utils().read_data(source_full_file_name)
    #     print('Input data source ')
    #     print(source_data)
    #
    #     # data preparation for swapping idea
    #
    #     # data_scoping = Utils().data_scoping(source_data, 'train')
    #     print(' all dataset before omar function', source_data.count())
    #     source_data = source_data[['Visit_3_Cat_1', 'Visit_2_Cat_1', 'Visit_1_Cat_1']]
    #     data_scoping = source_data.dropna(subset=['Visit_3_Cat_1', 'Visit_2_Cat_1', 'Visit_1_Cat_1'])
    #     # print(df.shape)
    #     # print(df.head())
    #     data_scoping = data_scoping.reset_index()
    #     del data_scoping['index']
    #     df = data_scoping.fillna(0)
    #
    #
    #     # data_scoping = Utils().data_preparation(source_data, 5, 3)
    #     print(' all dataset after omar function', data_scoping.count())
    #
    #     # data_scoping = Utils().visits_categories_columns(source_data, 1, 3)
    #     print(data_scoping)
    #     # if not (data_scoping['isSuccess']):
    #     #     return data_scoping
    #
    #     # if len(data_scoping[0]) == 0:
    #     #     return Utils().with_error(10, 'There is no training data available, check CanPredictChurn column')
    #
    #     # in_scope = data_scoping[0]
    #     # out_scope = all_data[1]
    #
    #     # Remove identifier and the label
    #     # in_scope_rm_id_label = in_scope[['CustomerId', 'ChurnValue']]
    #     # in_scope.drop(['CustomerId', 'ChurnValue'], axis=1, inplace=True)
    #     #
    #     # in_scope = CleaningData().cleaning_data(in_scope) # we reset the index
    #
    #     # report the training columns with customer_id
    #     # training_col = in_scope.columns
    #     # print('features_list_raw', training_col)
    #     # features_list = list(training_col)
    #     # print('features_list', features_list)
    #     # training_columns = features_list + ['CustomerId']
    #     # # print(training_columns)
    #     # print(in_scope_rm_id_label.head(2))
    #     print('------------------------checkssssssssssssss-------------------')
    #
    #     # source_data['CustomerId'] = in_scope_rm_id_label[['CustomerId']]
    #     # in_scope['ChurnValue'] = in_scope_rm_id_label[['ChurnValue']]
    #     # gk = in_scope.groupby('ChurnValue').count()
    #     # print(gk)
    #     # print(in_scope.shape)
    #     # creating instance of labelencoder
    #     # print(in_scope.head(2))
    #     # print(isinstance(in_scope, pd.DataFrame))
    #     # scaled_data = CNN().label_encoding(in_scope, 'ChurnValueCodes')
    #     # df_selected = scaled_data[0]
    #     # labelencoder = scaled_data[1]
    #
    #     # reset the index to the data
    #     # df_selected = df_selected.reset_index()
    #     # df_selected.drop(['index'], axis=1, inplace=True)
    #
    #     # check if the feature space is sparce and return error msg
    #     # from transformation
    #
    #     # Splitting the data 3 division train, validation and testing and reshaping the data
    #     # x_trn_reshaped, x_trn, y_trn, x_val_reshaped, x_val, y_val, x_tst_reshaped, x_tst, y_tst, scaler \
    #     #     = Transform().split_data(df_selected, 0.2, 'ChurnValueCodes')
    #     # x_trn_reshaped, x_train, y_train, x_val_reshaped, x_val, y_val, x_tst_reshaped, x_test, y_test
    #
    #     # x_trn, y_trn, x_val, y_val, x_tst, y_tst, y_columns = Transform().nbo_split_data\
    #     #     (data_scoping, 0.2, 'Visit_3_Cat_1')
    #     #
    #
    #     # x_trn_reshaped, x_trn, y_trn, x_val_reshaped, x_val, y_val, x_tst_reshaped, x_tst, y_tst\
    #     x_trn_reshaped, x_trn, y_trn, x_val_reshaped, x_val, y_val, x_tst_reshaped, x_tst, y_tst, y_columns, classes\
    #         = Transform().nbo_split_data_test(data_scoping, 0.5, 'Visit_3_Cat_1')
    #     print('y_columns:', y_columns)
    #     print('y_tst: ', y_tst)
    #
    #     # Training the model with auto trainer and auto evaluator
    #     # final_results = CNN().model_trainer(x_trn_reshaped, y_trn, x_val_reshaped, y_val, x_tst_reshaped, y_tst)
    #     # final_results = RNN().model_trainer(x_trn, y_trn, x_val, y_val, x_tst, y_tst)
    #
    #     final_results = RNN().model_trainer(x_trn_reshaped, y_trn, x_val_reshaped, y_val, x_tst_reshaped, y_tst, classes)
    #
    #     print('-------------final results-------------')
    #     print(final_results)
    #
    #     # save the model object with check option
    #     model_file_path = Utils().save_pipeline(final_results[2], Utils().generate_file_name('model'), client_name)
    #     # scaler_file_path = Utils().save_pickle(scaler, Utils().generate_file_name('scalar'), client_name)
    #
    #     # Delete the weights files after all experiments
    #     Utils().clean_best_model_file(client_name)
    #
    #     # return Utils.with_success({
    #     #     "scalerUrl": scaler_file_path,
    #     #     "modelUrl": model_file_path,
    #     #     "featuresList": training_columns,
    #     #     "predictionScore": round(final_results[1], 2)  # this should be reported on the testing sets
    #     # })
    #     return Utils.with_success({
    #         "modelUrl": model_file_path,
    #         # "featuresList": training_columns,
    #         "rnnType": final_results[2],
    #         "predictionScore": round(final_results[1], 2)  # this should be reported on the testing sets
    #     })
    #     # except Exception as err:
    #     #     return Utils().with_error(0, '', err)
    #
    # @classmethod
    # def predict(cls, source_full_file_name, model_file_name, client_name):
    #     # def predict(cls, source_full_file_name, model_file_name, scaler_file_name, training_columns, client_name):
    #
    #     """
    #     Method to predict CNN model for churn prediction data
    #     Args:
    #         source_full_file_name(str): scaler file full path
    #         model_file_name(str): model file full path
    #         scaler_file_name(str): columns that final model training on them
    #         training_columns(list): final model accuracy on the testing dataset
    #         client_name(str): client home directory name
    #     Returns:
    #         predictionFileUrl(str): output file full path
    #     """
    #
    #     # try:
    #     predict = NBO()
    #
    #     # read the data file
    #     source_data = Utils().read_data(source_full_file_name)
    #     # print(source_data.head(2))
    #
    #     Dummies = Transform().one_hot_encoding_data(source_data, x_features, number_of_vistis)
    #
    #
    #     # Should filter not applicable
    #     data_scoping = Utils().data_scoping(source_data, 'predict')
    #     # if not (data_scoping['isSuccess']):
    #     #     return data_scoping
    #
    #     # all_data = data_scoping['data']
    #     if len(data_scoping[0]) != 0:
    #         in_scope = data_scoping[0]
    #         out_scope = data_scoping[1]
    #
    #     # reading data for prediction
    #     df = in_scope[training_columns]
    #     # print(df.head(2))
    #
    #     # load the model object
    #     cnn_model = Utils().load_pipeline(model_file_name)
    #
    #     if not (cnn_model['isSuccess']):
    #         return cnn_model
    #
    #     cnn_model = cnn_model['data']
    #
    #     # load the scalar object
    #     cnn_scalar = Utils().load_pickle(scaler_file_name)
    #
    #     if not (cnn_scalar['isSuccess']):
    #         return cnn_scalar
    #
    #     cnn_scalar = cnn_scalar['data']
    #
    #     # reserve the customer id
    #     id_reservation = df[['CustomerId']]
    #
    #     # normalize the pipeline
    #     if not ('CustomerId' in df.columns):
    #         return Utils().with_error(6, 'The ID column does not exist')
    #     df = df.drop('CustomerId', axis=1)
    #     scaled_df = cnn_scalar.transform(df)
    #
    #     # predict the model
    #     pred_prob = predict.predict_fn(cnn_model, scaled_df)
    #     df['CustomerId'] = id_reservation
    #     # print(df.head(2))
    #     df['ChurnPred'] = pred_prob[0]
    #     df['ChurnProb'] = pred_prob[1]
    #     df.ChurnProb = df.ChurnProb.round(4)
    #
    #     in_scope = df[['CustomerId', 'ChurnPred', 'ChurnProb']]
    #
    #     # Combine the in scope and out scope data
    #     if len(out_scope) != 0:
    #         union_in_out_scope = pd.concat([in_scope, out_scope], ignore_index=True)
    #     else:
    #         union_in_out_scope = pd.concat([in_scope], ignore_index=True)
    #
    #     # save the prediction result in the file
    #     output_full_file_name = Utils().write_csv_file(union_in_out_scope, client_name)
    #
    #     # return the output
    #     return Utils().with_success({
    #         "predictionFileUrl": output_full_file_name
    #     })
    #
    #     # except Exception as err:
    #     #     return Utils().with_error(0, '', err)
