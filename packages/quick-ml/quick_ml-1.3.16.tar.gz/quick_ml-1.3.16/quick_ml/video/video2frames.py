class V2F():

    def __init__(self, output_folder):
        self.output_folder = output_folder



    def __get_fps(self, video_file):
        video = cv2.VideoCapture(video_file);

        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

        if int(major_ver)  < 3 :
            fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
            print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
        else:
            fps = video.get(cv2.CAP_PROP_FPS)
            print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

        video.release()

        return int(round(fps))



    def convert2frames(self, video_path, video_name, sparsify = True, frame_freq = None):
        assert os.path.isfile(video_path) == True
        
        if sparsify:
            #frame_freq = int(input("Please enter the save frequency for frames per second: \n"))
            assert frame_freq is not None 
            assert isinstance(frame_freq, int)

        cam = cv2.VideoCapture(video_path)

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder) 

        currentframe = 0
        min_time_counter = 1
        frame_counter = 0
        fps = self.__get_fps(video_path)
        intervals = random.sample(range(0, fps), frame_freq)
        random_intervals = []

        min_intervals = []
        for i in range(0, 60):
            for j in intervals:
                min_intervals.append(j + (fps*i))

        while(True):

            ret, frame = cam.read()

            if ret:
                frame_counter += 1

                name = f'{self.output_folder}/{video_name}/{str(min_time_counter)}/frame' + str(currentframe) + '.jpg'
                #print ('Creating...' + name)
                if not os.path.exists(self.output_folder + '/' + video_name + '/' + str(min_time_counter)):
                    os.makedirs(self.output_folder + '/' + video_name + '/' + str(min_time_counter))
  
                # writing the extracted images
                if sparsify == "yes" :
        
        
        
                    #if frame_counter % 60 == 0:
        
                    #if divisible(frame_counter, random_intervals):
                    #if frame_counter in random_intervals:
                    if frame_counter in min_intervals:
            
                        cv2.imwrite(name, frame)
                        print ('Creating...' + name)
                else:
                    cv2.imwrite(name, frame)
                    print ('Creating...' + name)


                # increasing counter so that it will
                # show how many frames are created
                currentframe += 1

                if frame_counter >= fps * 60:
                  #start_time = time.time()
                    min_time_counter += 1
                    frame_counter = 0

            else:
                break

        cam.release()
        cv2.destroyAllWindows()


    def extract_interval(self):
        pass 

    def extract_multi_intervals(self):
        pass
    

    def convert_batch2frames(self):
        pass

    def compress(self, output_file_name):

        zipf = zipfile.ZipFile(output_file_name, 'w', zipfile.ZIP_DEFLATED)
        self.__zipdir(self.output_folder, zipf)
        zipf.close()


    def __zipdir(self, path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                                           os.path.join(path, '..')))



if __name__ != "__main__":
    import os
    import cv2 
    import numpy as np 
    from tqdm import tqdm 
    from glob import glob
    import random
    import zipfile
    
      
