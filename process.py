import glob
import os
import json

from universalclassifier import predict

#INPUT_PATH = "/home/lhboulogne/Downloads/test/inout/input/images/"
#OUTPUT_PATH = "/home/lhboulogne/Downloads/test/inout/output/"
INPUT_PATH = "/input/images/"
OUTPUT_PATH = "/output/"


def save_name_from_interface(interface):
    #  Account for interfaces where the directory name (for input) or filename (for output) is different from the interface slug.
    if interface == "ct-image":
        return "ct"
    if interface == "oct-image":
        return "oct"
    if interface == "lobe-and-covid-19-lesion-segmentation":
        return "lobe-and-covid-19-lesion-segementation"
    if interface == "prostate-cancer-likelihood":
        return "cspca-case-level-likelihood"
    return interface


class Algorithm:
    def __init__(self, input_interfaces, output_interfaces, roi_segmentation_interface, artifact_path=None,
                 input_path="/input/images", output_path="/output"):
        if artifact_path is None:
            artifact_path = os.path.join(os.getcwd(), "artifact")
        self.input_interfaces = input_interfaces
        self.output_interfaces = output_interfaces
        self.roi_segmentation_interface = roi_segmentation_interface
        self.artifact_path = artifact_path
        self.input_path = input_path
        self.output_path = output_path

    def get_input_filename_for_interface(self, interface):
        interface_dir = os.path.join(self.input_path, save_name_from_interface(interface))
        files = list(glob.glob(os.path.join(interface_dir, "*")))
        if len(files) == 0:
            raise  RuntimeError(f"No file found for interface `{interface}` in `{interface_dir}`.")
        if len(files) > 1:
            raise RuntimeError(
                f"Expected only one file per input interface when processing each case. Found {len(files)} inputs for interface: {interface}. Aborting.")
        return files[0]

    def find_input_files(self):
        input_filenames = []
        for interface in self.input_interfaces:
            input_filenames.append(self.get_input_filename_for_interface(interface))

        if self.roi_segmentation_interface is not None:
            seg_filename = self.get_input_filename_for_interface(self.roi_segmentation_interface)
        else:
            seg_filename = None
        return input_filenames, seg_filename

    def save_outputs(self, outputs):
        if len(outputs) != len(self.output_interfaces):
            raise RuntimeError(
                f"Unexpected number of outputs. Found {len(outputs)} outputs for {len(self.output_interfaces)} interfaces, namely {self.output_interfaces}. Aborting.")
        for output, output_interface in zip(outputs, self.output_interfaces):
            with open(os.path.join(self.output_path, save_name_from_interface(output_interface) + '.json'), "w") as f:
                json.dump(output, f)

    def process(self):
        input_filenames, seg_filename = self.find_input_files()
        outputs = predict(self.artifact_path, input_filenames, seg_filename)
        self.save_outputs(outputs)


if __name__ == "__main__":
    with open("task_config.json", "r") as f:
        config = json.load(f)

    Algorithm(**config, input_path=INPUT_PATH, output_path=OUTPUT_PATH).process()
