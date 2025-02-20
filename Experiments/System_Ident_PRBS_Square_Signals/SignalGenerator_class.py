import numpy as np
import matplotlib.pyplot as plt

class SignalGenerator:
    def __init__(self, sample_rate=1.0):
        """
        Initialize signal generator with optional sample rate
        (default sample rate = 1.0 Hz)
        """
        self.sample_rate = sample_rate

    def generate_prbs(self, sequence_length: int, min_val: float, 
                     max_val: float, num_samples: int) -> np.ndarray:
        """
        Generate PRBS signal with specified parameters
        """
        # Validate sequence length
        if sequence_length not in {3, 4, 7}:
            raise ValueError("sequence_length must be 3, 4, or 7")

        # LFSR configuration
        lfsr_config = {
            3: {'n': 3, 'taps': [2, 1]},
            4: {'n': 4, 'taps': [3, 2]},
            7: {'n': 7, 'taps': [6, 5]}
        }
        
        config = lfsr_config[sequence_length]
        n, taps = config['n'], config['taps']
        max_seq_length = (1 << n) - 1

        # Generate base sequence
        state = (1 << n) - 1
        sequence = []
        
        for _ in range(max_seq_length):
            output_bit = (state >> (n - 1)) & 1
            sequence.append(output_bit)
            
            feedback = sum((state >> tap) & 1 for tap in taps) % 2
            state = ((state << 1) & ((1 << n) - 1)) | feedback

        # Create full signal
        repeats = num_samples // max_seq_length
        remainder = num_samples % max_seq_length
        
        signal = np.array(sequence * repeats + sequence[:remainder], dtype=np.float64)
        return np.where(signal == 0, min_val, max_val)

    def generate_square(self, high_duration: float, low_duration: float,
                       min_val: float, max_val: float, total_duration: float) -> np.ndarray:
        """
        Generate square wave signal with specified parameters
        (durations in seconds)
        """
        # Calculate samples per phase
        high_samples = int(high_duration * self.sample_rate)
        low_samples = int(low_duration * self.sample_rate)
        
        if high_samples <= 0 or low_samples <= 0:
            raise ValueError("Durations must result in at least 1 sample per phase")

        # Create one period
        period = np.concatenate([
            np.full(high_samples, max_val),
            np.full(low_samples, min_val)
        ])
        
        # Calculate total number of periods needed
        total_samples = int(total_duration * self.sample_rate)
        num_periods = total_samples // len(period)
        remainder = total_samples % len(period)
        
        # Generate signal
        signal = np.tile(period, num_periods)
        if remainder > 0:
            signal = np.concatenate([signal, period[:remainder]])
            
        return signal

# Example usage
if __name__ == "__main__":
    # Initialize generator with 100 Hz sample rate
    gen = SignalGenerator(sample_rate=1)
    
    # Generate PRBS7 signal
    prbs = gen.generate_prbs(
        sequence_length=7,
        min_val=-1,
        max_val=1,
        num_samples=1000
    )
    
    # Generate square wave (0.5Hz, 50% duty cycle)
    square = gen.generate_square(
        high_duration=20.0,  # 1 second high
        low_duration=20.0,   # 1 second low
        min_val=-1,
        max_val=1,
        total_duration=100   # 20 second signal
    )
    
    # Plot results
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    
    # Plot PRBS
    ax1.plot(prbs[:200])
    ax1.set_title("PRBS7 Signal (First 200 Samples)")
    ax1.set_ylabel("Amplitude")
    
    # Plot Square Wave
    ax2.plot(square[:400])  # Show first 4 seconds (400 samples at 100Hz)
    ax2.set_title("Square Wave Signal (First 4 Seconds)")
    ax2.set_ylabel("Amplitude")
    ax2.set_xlabel("Samples")
    
    plt.tight_layout()
    plt.show()