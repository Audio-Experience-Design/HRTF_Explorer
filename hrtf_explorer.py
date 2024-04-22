'''
hrtf_explorer uses the BRT toolbox to render 
'''
import subprocess
import numpy as np
import argparse
from pythonosc import udp_client
import tkinter as tk
import customtkinter as ctk
from PIL import Image
import yaml
import time
from spatialaudiometrics import angular_metrics as am

class HRTFselection(ctk.CTkFrame):
    '''
    Radio buttons to select the HRTF as defined in the yml configuration file
    '''
    def hrtf_radiobutton_event(self):
        '''
        Assign the listener to a different hrtf
        '''
        value = self.radio_var.get()
        self.master.client.send_message("/listener/setHRTF", ["DefaultListener", "HRTF"+ str(value)])

    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        curr_column = 0

        label           = ctk.CTkLabel(self, text = "Select HRTF: ", fg_color = "transparent", text_color = "white" , font = ("Arial", 16,"bold"))
        label.grid(row=0, column=curr_column, padx=10, pady=10)

        radiobutton_dict = dict()
        self.radio_var = tk.IntVar(value=0)
        for h, hrtf in enumerate(self.master.config['hrtfs']):
            self.master.client.send_message("/loadHRTF", ["HRTF"+str(h), self.master.config['hrtf_dir'] + hrtf,self.master.config['hrtf_resampling_step']])
            radiobutton_dict[str(h)] = ctk.CTkRadioButton(self, text=hrtf, command=self.hrtf_radiobutton_event, variable= self.radio_var, value=h)
            radiobutton_dict[str(h)].grid(row=8+h, column=curr_column, padx=50, pady=5,sticky = 'W')
        self.master.client.send_message("/listener/setHRTF", ["DefaultListener", "HRTF0"])

class ListenerLocation(ctk.CTkFrame):
    '''
    Widgets for defining the listener position
    '''
    def x_slider_event(self,value):
        '''
        Changes the x of the listener
        '''
        self.x_label.configure(text = 'X: ' + str(np.round(value,1)))
        self.master.x_loc = value
        self.master.client.send_message("/listener/location",["DefaultListener",self.master.x_loc,self.master.y_loc,self.master.z_loc])

    def y_slider_event(self,value):
        '''
        Changes the y of the listener
        '''
        self.y_label.configure(text = 'Y: ' + str(np.round(value,1)))
        self.master.y_loc = value
        self.master.client.send_message("/listener/location",["DefaultListener",self.master.x_loc,self.master.y_loc,self.master.z_loc])
        
    def z_slider_event(self,value):
        '''
        Changes the z of the listener
        '''
        self.z_label.configure(text = 'Z: ' + str(np.round(value,1)))
        self.master.z_loc = value
        self.master.client.send_message("/listener/location",["DefaultListener",self.master.x_loc,self.master.y_loc,self.master.z_loc])

    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        curr_column = 0
        label           = ctk.CTkLabel(self, text = "Listener location: ", fg_color = "transparent", text_color = "white" , font = ("Arial", 16,"bold"))
        label.grid(row=4, column=curr_column, padx=10, pady=10)
        self.x_label    = ctk.CTkLabel(self, text = "X: 0", fg_color = "transparent", text_color = "white" , font = ("Arial", 12))
        self.x_label.grid(row=5, column=curr_column, padx=10, pady=10)
        x_slider        = ctk.CTkSlider(self, from_=-1.5, to=1.5, command=self.x_slider_event)
        x_slider.grid(row=6, column=curr_column, padx=5, pady=5)
        x_slider.set(0)

        self.y_label    = ctk.CTkLabel(self, text = "Y: 0", fg_color = "transparent", text_color = "white" , font = ("Arial", 12))
        self.y_label.grid(row=7, column=curr_column, padx=10, pady=10)
        y_slider        = ctk.CTkSlider(self, from_=-1.5, to=1.5, command=self.y_slider_event)
        y_slider.grid(row=8, column=curr_column, padx=5, pady=5)
        y_slider.set(0)

        self.z_label = ctk.CTkLabel(self, text = "Z: 0", fg_color = "transparent", text_color = "white" , font = ("Arial", 12))
        self.z_label.grid(row=9, column=curr_column, padx=10, pady=10)
        z_slider = ctk.CTkSlider(self, from_=-1.5, to=1.5, command=self.z_slider_event)
        z_slider.grid(row=10, column=curr_column, padx=5, pady=5)
        z_slider.set(0)

class SourceLocation(ctk.CTkFrame):
    '''
    Widgets for defining source position
    '''
    def az_slider_event(self,value):
        '''
        Changes the azimuth of the source
        '''
        self.az_label.configure(text = 'Azimuth: ' + str(np.round(value,1)))
        self.master.az_loc = value
        x,y,z = am.polar2cartesian(self.master.az_loc,self.master.el_loc,self.master.dist_loc)
        self.master.client.send_message("/source/location",["source1",x,y,z])

    def el_slider_event(self,value):
        '''
        Changes the azimuth of the source
        '''
        self.el_label.configure(text = 'Elevation: ' + str(np.round(value,1)))
        self.master.el_loc = value
        x,y,z = am.polar2cartesian(self.master.az_loc,self.master.el_loc,self.master.dist_loc)
        self.master.client.send_message("/source/location",["source1",x,y,z])

    def dist_slider_event(self,value):
        '''
        Changes the azimuth of the source
        '''
        self.dist_label.configure(text = 'Distance: ' + str(np.round(value,1)))
        self.master.dist_loc = value
        x,y,z = am.polar2cartesian(self.master.az_loc,self.master.el_loc,self.master.dist_loc)
        self.master.client.send_message("/source/location",["source1",x,y,z])

    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        curr_column = 0
        label           = ctk.CTkLabel(self, text = "Source 1 location: ", fg_color = "transparent", text_color = "white" , font = ("Arial", 16,"bold"))
        label.grid(row=4, column=curr_column, padx=10, pady=10)
        self.az_label   = ctk.CTkLabel(self, text = "Azimuth: 0", fg_color = "transparent", text_color = "white" , font = ("Arial", 12))
        self.az_label.grid(row=5, column=curr_column, padx=5, pady=5)
        az_slider       = ctk.CTkSlider(self, from_=0, to=360, command=self.az_slider_event)
        az_slider.grid(row=6, column=curr_column, padx=5, pady=5)
        az_slider.set(0)

        self.el_label   = ctk.CTkLabel(self, text = "Elevation: 0", fg_color = "transparent", text_color = "white" , font = ("Arial", 12))
        self.el_label.grid(row=7, column=curr_column, padx=5, pady=5)
        el_slider = ctk.CTkSlider(self, from_=-90, to=90, command=self.el_slider_event)
        el_slider.grid(row = 8, column=curr_column, padx=5, pady=5)
        el_slider.set(0)

        self.dist_label = ctk.CTkLabel(self, text = "Distance: 1.5", fg_color = "transparent", text_color = "white" , font = ("Arial", 12))
        self.dist_label.grid(row=9, column=curr_column, padx=5, pady=5)
        dist_slider     = ctk.CTkSlider(self, from_=0.1, to=5, command=self.dist_slider_event)
        dist_slider.grid(row=10, column=curr_column, padx=5, pady=5)
        dist_slider.set(1.5)

class GUI(ctk.CTk):
    '''
    GUI for exploring the hrtfs
    '''

    def load_config_file(self):
        '''
        Loads in the parameters for hrtf explorer
        '''
        with open('config.yml', 'r') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        return config

    def setup_osc_connections(self,port):
        '''
        Initialises connections with max
        '''
        # Set up connection with MaxPatch
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=port, help="The port the OSC server is listening on")
        args_max = parser.parse_args()
        client = udp_client.SimpleUDPClient(args_max.ip, args_max.port)
        return client


    def gain_slider_event(self,value):
        '''
        Changes the overall volume
        '''
        self.curr_gain = value
        self.gain_label.configure(text = 'Overall Gain (dB): ' + str(np.round(value,1)))
        self.client.send_message("/source/gain",["source1",value])
        self.client.send_message("/source/gain",["source2",value])

    def play_sound(self):
        '''
        Play the sound loaded
        '''
        self.client.send_message("/play",[])

    def stop_sound(self):
        '''
        Stop the sound loaded
        '''
        self.client.send_message("/stop",[])

    def record_sound(self):
        '''
        Play and record the sound
        '''
        self.client.send_message("/playAndRecord",["C:/GitHubRepos/Spatial-Audio-Experiments/temp.mat", "mat", 5])

    def near_field(self):
        '''
        Enables near field rendering
        '''
        value = self.near_field_check.get()
        self.client.send_message("/listener/enableNearFieldEffect",["DefaultListener", value])

    def spatialisation(self):
        '''
        Enables spatialisation
        '''
        value = self.spat_check.get()
        self.client.send_message("/listener/enableSpatialization",["DefaultListener", value])

    def mute_sound(self):
        '''
        Mutes the audio
        '''
        value = self.mute_check.get()
        if value:
            self.client.send_message("/source/mute","source1")
            self.client.send_message("/source/mute","source2")
        else:
            self.client.send_message("/source/unmute","source1")
            self.client.send_message("/source/unmute","source1")

    def second_source(self):
        '''
        Adds a second source
        '''
        value = self.source2_check.get()
        stim = self.config['source2_stim']

        if value:
            self.client.send_message("/source/loadSource",["source2",stim])
            self.client.send_message("/source/gain",["source2",self.curr_gain])
            x,y,z = am.polar2cartesian(0,0,1.5)
            self.client.send_message("/source/location",["source2",x,y,z])
            self.client.send_message("/source/play","source2")
        else:
            self.client.send_message("/source/stop","source2")
            self.client.send_message("/source/removeSource","source2")


    def __init__(self):
        '''
        Initialises gui
        '''
        #ctk.CTk.__init__(self)
        super().__init__()

        # Load in the config
        self.config = self.load_config_file()

        # Start the BERTA app
        self.berta = subprocess.Popen(self.config['brt_dir'])
        print('Waiting whilst BRT opens...')
        time.sleep(4)

        # Set up OSC connection
        self.client = self.setup_osc_connections(self.config['brt_send_port'])
        self.client.send_message("/control/connect",[str(self.config['brt_ip']),self.config['brt_receive_port']])
        self.client.send_message("/removeAllSources",[])

        # Initialise audio on BRT
        self.client.send_message("/source/loadSource",["source1",self.config['source1_stim'],""])
        self.az_loc     = 0
        self.el_loc     = 0
        self.dist_loc   = 1.5
        self.curr_gain  = 0
        self.x_loc      = 0
        self.y_loc      = 0
        self.z_loc      = 0
        x,y,z = am.polar2cartesian(self.az_loc,self.el_loc,self.dist_loc)
        self.client.send_message("/source/location",["source1",x,y,z])

        # Set up the GUI
        ctk.set_appearance_mode("dark")
        self.title("HRTF explorer")
        self.geometry("1500x700")

        # Set up text
        label = ctk.CTkLabel(self, text = "")
        label.grid(row = 0, padx=20, pady=20)
        label = ctk.CTkLabel(self, text = "HRTF Explorer",fg_color = "transparent", text_color = "white" , font = ("Arial", 30, "bold"))
        label.grid(row = 1, column = 2, columnspan = 4, padx=20, pady=20)
        image = ctk.CTkImage(light_image = Image.open("./images/sonicom_logo_bw.png"), size = (1140/5, 235/5))
        logo = ctk.CTkLabel(self, image=image, text = "")
        logo.grid(row = 2, column = 1, padx=20, pady=20, stick = 'E')

        label = ctk.CTkLabel(self, text = "Created by Katarina C. Poole \n(Audio Experience Design Team at Imperial College London)", fg_color = "transparent", text_color = "white" , font = ("Arial", 14, "italic"), justify = 'right')
        label.grid(row = 2, column = 2, columnspan = 4, padx=20, pady=20, stick = 'E')
        image = ctk.CTkImage(light_image = Image.open("./images/axd_logo.png"), size = (100, 100))
        logo = ctk.CTkLabel(self, image=image, text = "")
        logo.grid(row = 2, column = 6, padx=20, pady=20, stick = 'E')
        label = ctk.CTkLabel(self, text = "")
        label.grid(row = 0, column = 0, padx=20, pady=20)

        # Set up play and stop buttons and HRTF radio buttons
        curr_column = 1
        button_play = ctk.CTkButton(self, text="Play",  fg_color = 'green', text_color = 'white', font = ("Arial",20,'italic'), command = self.play_sound)
        button_play.grid(row=4, column=curr_column, padx=50, pady=20,sticky = 'W')
        button_stop = ctk.CTkButton(self, text="Stop",  fg_color = 'red', text_color = 'white', font = ("Arial",20,'italic'), command = self.stop_sound)
        button_stop.grid(row=5, column=curr_column, padx=50, pady=20,sticky = 'W')
        button_play_rec = ctk.CTkButton(self, text="Play & record",  fg_color = 'orange', text_color = 'white', font = ("Arial",20,'italic'), command = self.record_sound)
        button_play_rec.grid(row=6, column=curr_column, padx=50, pady=20,sticky = 'W')

        # Set up hrtf selection
        self.hrtf_frame = HRTFselection(master=self)
        self.hrtf_frame.grid(row=4, rowspan = 4, column=2, padx=20, pady=20,sticky='nsew')

        # Set up az and el source sliders
        self.positions_frame = SourceLocation(master=self)
        self.positions_frame.grid(row=4, rowspan = 4, column=3, padx=20, pady=20,sticky='nsew')

        # Set up x,y,z listener sliders
        self.listener_frame = ListenerLocation(master=self)
        self.listener_frame.grid(row=4, rowspan = 4, column=4, padx=20, pady=20,sticky='nsew')

        # Set up enable check boxes
        curr_column = 5
        self.near_field_check   = ctk.BooleanVar(value=True)
        near_field_check_box    = ctk.CTkSwitch(self, text="Enable Near Field", command=self.near_field, variable=self.near_field_check, onvalue=1, offvalue=0)
        near_field_check_box.grid(row=4, column=curr_column, padx=10, pady=10,sticky = 'W')

        self.spat_check         = ctk.IntVar(value=1)
        spat_check_box          = ctk.CTkSwitch(self, text="Enable Spatialisation", command=self.spatialisation, variable=self.spat_check, onvalue=1, offvalue=0)
        spat_check_box.grid(row=5, column=curr_column, padx=10, pady=10,sticky = 'W')

        self.mute_check         = ctk.BooleanVar(value=False)
        mute_check_box          = ctk.CTkSwitch(self, text="Mute", command=self.mute_sound, variable=self.mute_check, onvalue=True, offvalue=False)
        mute_check_box.grid(row=6, column=curr_column, padx=10, pady=10,sticky = 'W')

        self.source2_check      = ctk.BooleanVar(value=False)
        source2_check_box       = ctk.CTkSwitch(self, text="Source 2", command=self.second_source, variable=self.source2_check, onvalue=True, offvalue=False)
        source2_check_box.grid(row=7, column=curr_column, padx=10, pady=10,sticky = 'W')

        # Gain slider
        curr_column = 6
        self.gain_label         = ctk.CTkLabel(self, text = "Overall Gain (dB): 0", fg_color = "transparent", text_color = "white" , font = ("Arial", 12))
        self.gain_label.grid(row=4, column=curr_column, padx=10, pady=10)
        gain_slider             = ctk.CTkSlider(self, from_=-20, to=0, command=self.gain_slider_event,orientation = 'vertical')
        gain_slider.grid(row=5, column=curr_column, padx=10, pady=10, rowspan = 3)
        gain_slider.set(0)

        label = ctk.CTkLabel(self, text = "")
        label.grid(row = 0, column = 7, padx=20, pady=20)


    def __enter__(self):
        print("Starting HRTF Explorer...")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.berta.terminate()
        print("Closed HRTF Explorer")

def main():
    '''
    Opens the GUI
    '''
    app = GUI()
    with app:
        app.mainloop()

if __name__ == "__main__":
    main()
    